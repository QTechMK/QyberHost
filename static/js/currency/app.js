let rtCurrencyConverter = {
    init: function () {
        this.getBaseCurrency();
        this.getCurrencies();
        // this.fetchAndStoreCurrency();
        this.loadCurrencyConfig();
        this.convertAllPricesCurrency();
    },

    getBaseCurrency: function () {
        // check LocalStorage
        let storedCurrency = localStorage.getItem('defaultCurrency');

        if (storedCurrency) {
            return storedCurrency;
        }

        // load from json if not existing
        return fetch('static/js/currency/configue.json')
            .then(response => response.json())
            .then(data => {
                let defaultCurrency = data.defaultCurrency || 'usd'; 
                localStorage.setItem('defaultCurrency', defaultCurrency); // save to localStorage
                return defaultCurrency;
            })
            .catch(error => {
                return 'usd'; // return 'usd' if any problem
            });
    },
    updateUserPreferedCurrency: function (selectedCurreny = 'usd') { 
        localStorage.setItem('updateUserPreferedCurrency', selectedCurreny);
    },
    getUserPreferedCurrency: async function () { 

        let userPreferedCurrency = localStorage.getItem('updateUserPreferedCurrency');
        if(userPreferedCurrency) {
            return userPreferedCurrency;
        }

        const config = await this.getCurrencyConfig();
        userPreferedCurrency = config.defaultCurrency;
        return userPreferedCurrency;

    },
    getCurrencySymbol: function (currencyCode) {
        return fetch('static/js/currency/currencies.json')
            .then(response => response.json())
            .then(data => {
                // Find the currency object that matches the given currencyCode
                let currency = data.find(item => item.cc === currencyCode);
    
                if (currency) {
                    return currency.symbol; // Assuming each object has a "symbol" key
                } else {
                    return '$'; // Default symbol if not found
                }
            })
            .catch(error => {
                return '$'; // Default symbol on error
            });
    },
    fetchAndStoreCurrency: function () {
        const fromCurrency = this.getBaseCurrency();
        const apiUrl = `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {

                let currencies = {};
                for (let key in data) {
                    if (data[key]) {
                        currencies[key] = data[key];
                    }
                }

                // save data to localstorage
                localStorage.setItem('currencies', JSON.stringify(currencies));
                localStorage.setItem('lastFetchedDate', new Date().toISOString().split('T')[0]);
            })
            .catch(error => console.error('Error fetching currencies:', error));
    },

    getCurrencies: function () {
        const lastFetchedDate = localStorage.getItem('lastFetchedDate');
        const today = new Date().toISOString().split('T')[0];

        // update data if not existing
        if (lastFetchedDate !== today) {
            
            this.fetchAndStoreCurrency();
            return JSON.parse(localStorage.getItem('currencies'));
        } else {
           
            const storedCurrencies = JSON.parse(localStorage.getItem('currencies'));
           
            return storedCurrencies;
        }
    },

    loadCurrencyConfig: async function () {
        fetch('static/js/currency/configue.json')
            .then(response => response.json())
            .then(data => {
                const selectElement = document.querySelector('.easy-currency-switcher-select');
                if (data.supportedCurrencies) {
                    data.supportedCurrencies.forEach(currency => {
                        const option = document.createElement('li');
                        option.setAttribute('data-value', currency);
                        option.classList.add('option');
                        option.textContent = currency.toUpperCase(); // convert to capital letter
                        selectElement.appendChild(option);
                    });

                    // select default currency
                    selectElement.value = data.defaultCurrency;
                }

                let options = document.querySelectorAll('.easy-currency-switcher-select li');

                options.forEach( option => {
                    option.addEventListener('click', function () { 
                        let selectedCurreny = this.getAttribute('data-value');
                        rtCurrencyConverter.updateUserPreferedCurrency(selectedCurreny);
                        location.reload();
                    })
                });

               
            })
            .catch(error => console.error('Error loading JSON file:', error));
            let userPreferedCurrency = await rtCurrencyConverter.getUserPreferedCurrency();
            document.querySelector('.easy-currency-switcher-toggle .currency-code').innerHTML = userPreferedCurrency;

    },

    getCurrencyConfig: async function () {
        try {
            const response = await fetch('static/js/currency/configue.json');
            const config = await response.json();
            return config;
        } catch (error) {
            return { baseCurrency: 'usd', currency_thousand_separator: '.', currency_decimal_separator: '' };
        }
    },

    detectThousandSeparator: function (value) {
        let cleanValue = value.replace(/[^\d.,]/g, '');
        if (cleanValue.includes(',') && cleanValue.includes('.')) {
            return cleanValue.lastIndexOf(',') < cleanValue.lastIndexOf('.') ? ',' : '.';
        } else if (cleanValue.includes(',')) {
            return ',';
        } else if (cleanValue.includes('.')) {
            return '.';
        }
        return null;
    },

    convertCurrency: async function (fromCurrency, toCurrency, value) {

        const config = await this.getCurrencyConfig();

        fromCurrency = fromCurrency || this.getBaseCurrency();

        let rates = await this.getCurrencies();
        rates = rates[fromCurrency];

        let convertedValue = value;
        let currencyThousandSeparator = config.currency_thousand_separator || '.';
        let currencyDecimalSeparator = config.currency_decimal_separator || '';

        if (rates && value) {
            let valueThousandSeparator = this.detectThousandSeparator(value);
            if (valueThousandSeparator === ',') {
                value = value.replace(/,/g, '.'); // Normalize to standard decimal format
            }

            value = parseFloat(value); // Convert to a float

            if (value > 0 && toCurrency !== 'custom_currency') {
                if (rates[toCurrency]) {
                    convertedValue = rates[toCurrency] * value;
                }
            }
        }
        convertedValue = convertedValue.toFixed(2);

        // Format the number with separators
        convertedValue = convertedValue.replace('.', currencyThousandSeparator);

        return convertedValue;
    },
    convertAllPricesCurrency: async function () {
        let userPreferedCurrency = await rtCurrencyConverter.getUserPreferedCurrency();
        let userPreferedCurrencySymbol = await rtCurrencyConverter.getCurrencySymbol( userPreferedCurrency.toUpperCase());
        let allPricesEl = document.querySelectorAll('[rt-price]');
        let allCurrencySymbolsEl = document.querySelectorAll('[rt-currency-symbol]');
    
        // update currency symbol
        allCurrencySymbolsEl.forEach(currencySymbolsEl => {
            currencySymbolsEl.innerHTML = userPreferedCurrencySymbol;

        });

        // update price
        allPricesEl.forEach(priceEl => {

            let price = priceEl.textContent;

            // Convert all prices
            rtCurrencyConverter.convertCurrency('', userPreferedCurrency, price).then((result) => {
                priceEl.textContent = result;
            });

        });

    }
    
    
};

// Initialize the currency converter
rtCurrencyConverter.init();







