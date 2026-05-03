from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import SignInForm, SignUpForm
from .models import UserProfile


KNOWLEDGEBASE_ARTICLES = [
    {
        'slug': 'wordpress-backdoor-eklenti-riskleri',
        'title': 'WordPress Arka Kapi Yaratan En Tehlikeli Eklenti Gruplari',
        'category': 'WordPress',
        'date': '12 Nisan 2026',
        'read_time': '6 dk okuma',
        'image': 'images/blog/blog-4.png',
        'summary': 'WordPress kurulumlarinda backdoor olusturan riskli eklenti ailelerini, erken belirtileri ve guvenli temizlik adimlarini ozetler.',
        'intro': 'WordPress ekosistemi buyudukce zararli kod enjekte eden eklenti kaliplari daha sofistike hale geliyor. Bu rehberde risk isaretlerini, kontrol adimlarini ve guvenli iyilestirme akislarini toplu bicimde ele aliyoruz.',
        'sections': [
            {
                'heading': 'En sik gorulen risk sinyalleri',
                'body': 'Beklenmeyen yonetici hesaplari, supheli cron gorevleri, tema klasorlerinde gizlenmis PHP dosyalari ve olagandisi cikis trafigi ilk kontrol edilmesi gereken alanlardir.',
            },
            {
                'heading': 'Temizleme ve sertlestirme plani',
                'body': 'Dosya butunlugu kontrolu, eklenti kaynak dogrulamasi, yonetici oturumlarinin sifirlanmasi ve WAF kurallari ile kalici guvenlik seviyesini yukseltmek mumkundur.',
            },
        ],
        'tags': ['WordPress', 'Guvenlik', 'Backdoor', 'Eklenti'],
    },
    {
        'slug': 'dnssec-nedir-nasil-kurulur',
        'title': 'DNSSEC Nedir ve Nasil Kurulur?',
        'category': 'Domain & Hosting',
        'date': '28 Mart 2026',
        'read_time': '5 dk okuma',
        'image': 'images/blog/blog-5.png',
        'summary': 'DNS kayitlarinin butunlugunu koruyan DNSSEC yapisini, kurulum adimlarini ve dogrulama kontrollerini anlatir.',
        'intro': 'DNSSEC, kullaniciyi sahte DNS cevaplarindan korumak icin gelistirilmis kritik bir imza mekanizmasidir. Ozellikle kurumsal domainlerde guvenilir cozumleme icin onemli bir savunma katmani saglar.',
        'sections': [
            {
                'heading': 'DNSSEC neden gereklidir?',
                'body': 'Ozellikle mail, musteri paneli ve odeme sayfalari barindiran alan adlarinda sahte yonlendirme riskini azaltir ve guven zincirini guclendirir.',
            },
            {
                'heading': 'Kurulum sonrasi yapilacak kontroller',
                'body': 'Registrar tarafindaki DS kaydi, nameserver uzerindeki DNSKEY bilgileri ve harici dogrulama araclari ile yapilandirmanin tutarli calistigi dogrulanmalidir.',
            },
        ],
        'tags': ['DNSSEC', 'Domain', 'DNS', 'Guvenlik'],
    },
    {
        'slug': 'mariadb-mysql-farklari',
        'title': 'MariaDB ve MySQL Arasindaki Farklar Nelerdir?',
        'category': 'Bilim ve Teknoloji',
        'date': '14 Mart 2026',
        'read_time': '7 dk okuma',
        'image': 'images/blog/blog-12.png',
        'summary': 'MariaDB ve MySQLi performans, lisanslama, uyumluluk ve yonetim araclari acisindan karsilastirir.',
        'intro': 'Her iki veritabani da benzer sozdizimine sahip olsa da surum politikalari, motor tercihleri ve performans stratejileri acisindan ayrisirlar.',
        'sections': [
            {
                'heading': 'Uyumluluk ve gecis kolayligi',
                'body': 'Bir cok uygulama icin gecis kolay gorunse de indeksleme, optimizer davranisi ve eklenti destegi gibi basliklarda detayli test yapmak gerekir.',
            },
            {
                'heading': 'Hangi senaryoda hangisi daha uygun?',
                'body': 'Yogun replikasyon, acik kaynak odakli tercih ve farkli storage engine gereksinimlerinde MariaDB one cikabilir; ticari ekosistem uyumlulugunda ise MySQL daha uygun olabilir.',
            },
        ],
        'tags': ['MariaDB', 'MySQL', 'Veritabani', 'Performans'],
    },
    {
        'slug': 'cpanel-domain-userdata-file-missing',
        'title': "cPanel 'domain userdata file appears to be missing' Hatasi Cozumu",
        'category': 'Sunucu',
        'date': '22 Subat 2026',
        'read_time': '4 dk okuma',
        'image': 'images/blog/blog-13.png',
        'summary': 'cPanel tarafinda eksik userdata dosyasi hatasini hizli teshis edip servis butunlugunu geri getirme adimlarini listeler.',
        'intro': 'Bu hata cogu zaman hesap tasima, basarisiz restore veya bozulmus metadata sonrasi gorulur. Sorunu dogru sirayla ele almak kesinti suresini ciddi bicimde azaltir.',
        'sections': [
            {
                'heading': 'Ilk dogrulama adimlari',
                'body': 'Hesabin userdata dizini, Apache include kayitlari ve cPanel rebuild komutlari kontrol edilerek eksik yapi taslari tespit edilmelidir.',
            },
            {
                'heading': 'Kalici duzeltme yaklasimi',
                'body': 'Yedekten geri yukleme, hesap metadata senkronizasyonu ve ilgili servislerin kontrollu yeniden baslatilmasi ile sistem yeniden tutarli duruma getirilebilir.',
            },
        ],
        'tags': ['cPanel', 'Sunucu', 'Hosting', 'Hata Cozumu'],
    },
    {
        'slug': 'cdn-nedir-site-hizina-etkisi',
        'title': 'CDN Nedir? Site Hizini ve Performansini Nasil Etkiler?',
        'category': 'Nedir? Nasil?',
        'date': '10 Ocak 2026',
        'read_time': '5 dk okuma',
        'image': 'images/blog/blog-14.png',
        'summary': 'CDN kullaniminin hiz, onbellekleme, uptime ve ziyaretci deneyimine etkisini pratik orneklerle aciklar.',
        'intro': 'CDN sadece statik dosya dagitimi degil, guvenlik ve yuk azaltma acisindan da guclu bir katmandir. Dogru kurulumla hem performans hem de dayaniklilik artar.',
        'sections': [
            {
                'heading': 'Performans tarafindaki katki',
                'body': 'Statik iceriklerin kullaniciya yakin edge noktalarindan servis edilmesi ilk byte suresini ve genel sayfa yuklenme surelerini dusurur.',
            },
            {
                'heading': 'Operasyonel kazanimlar',
                'body': 'Ani trafik yukselislerinde origin sunucunun yuku azalir, bazi saldiri tiplerinde koruma yuzeyi genisler ve kesinti riski duser.',
            },
        ],
        'tags': ['CDN', 'Performans', 'Cache', 'Web'],
    },
    {
        'slug': 'cloudflare-nedir',
        'title': 'Cloudflare Nedir? Nasil Calisir?',
        'category': 'Nedir? Nasil?',
        'date': '2 Aralik 2025',
        'read_time': '5 dk okuma',
        'image': 'images/blog/blog-6.png',
        'summary': 'Cloudflarein DNS, cache, WAF ve DDoS koruma katmanlarini sade bir dille aciklar.',
        'intro': 'Cloudflare, performans ve guvenligi ayni anda artirmak icin en sik kullanilan edge servislerinden biridir. Dogru kurgulandiginda teknik ekipler icin guclu bir operasyon yardimcisina donusur.',
        'sections': [
            {
                'heading': 'Temel servis katmanlari',
                'body': 'DNS yonetimi, onbellekleme, SSL terminasyonu ve WAF kurallari panel uzerinden birbirini tamamlayan bir yapi sunar.',
            },
            {
                'heading': 'Yanlis yapilandirmada gorulen sorunlar',
                'body': 'Cache bypass eksikleri, gercek IP gorunurlugu kaybi veya loop olusturan SSL modlari en sik karsilasilan sorunlardandir.',
            },
        ],
        'tags': ['Cloudflare', 'WAF', 'DNS', 'CDN'],
    },
    {
        'slug': 'alan-adi-transferi-nasil-yapilir',
        'title': 'Alan Adi Transferi Nasil Yapilir?',
        'category': 'Domain',
        'date': '18 Kasim 2025',
        'read_time': '4 dk okuma',
        'image': 'images/blog/blog-7.png',
        'summary': 'Domain transferi oncesi kilit acma, EPP kodu alma ve nameserver surekliligi gibi kritik adimlari ozetler.',
        'intro': 'Alan adi transferlerinde teknik akis kadar zamanlama da onemlidir. Yanlis planlama, e-posta veya web erisiminde kesinti riskini artirabilir.',
        'sections': [
            {
                'heading': 'Transfer oncesi kontrol listesi',
                'body': 'Registrar lock durumu, yonetici e-posta erisimi, EPP kodu ve son yenileme tarihi onceden dogrulanmalidir.',
            },
            {
                'heading': 'Kesintisiz transfer icin ipuclari',
                'body': 'Nameserver degisikligini transfer surecinden bagimsiz planlamak ve WHOIS dogrulama adimlarini geciktirmemek sureci hizlandirir.',
            },
        ],
        'tags': ['Domain', 'Transfer', 'EPP', 'Registrar'],
    },
    {
        'slug': 'sunucu-ve-bilgisayar-farklari',
        'title': 'Bilgisayarlar ve Sunucular Arasindaki Farklar Nelerdir?',
        'category': 'Sunucu',
        'date': '6 Ekim 2025',
        'read_time': '5 dk okuma',
        'image': 'images/blog/blog-8.png',
        'summary': 'Sunucu donanimi ile masaustu sistemler arasindaki mimari, erisilebilirlik ve kullanim farklarini karsilastirir.',
        'intro': 'Sunucular kesintisiz calisma, uzaktan yonetim ve olceklenebilirlik icin tasarlanir. Bu nedenle hem donanim hem de yazilim katmaninda daha farkli onceliklerle gelirler.',
        'sections': [
            {
                'heading': 'Donanim tarafindaki farklar',
                'body': 'ECC RAM, RAID kontrolculeri, yedekli guc kaynaklari ve out-of-band yonetim ozellikleri sunucu sinifi sistemlerin temel ayrisma alanlaridir.',
            },
            {
                'heading': 'Operasyonel kullanim farklari',
                'body': 'Sunucular ayni anda cok sayida kullaniciya servis verir; bu yuzden erisilebilirlik, izleme ve bakim penceresi yonetimi masaustu sistemlere gore cok daha kritiktir.',
            },
        ],
        'tags': ['Sunucu', 'Donanim', 'VDS', 'Operasyon'],
    },
]

KNOWLEDGEBASE_CATEGORIES = [
    'Bilim ve Teknoloji Dunyasi',
    'Nedir? Nasil?',
    'Domain & Hosting',
    'WordPress',
    'Sunucu',
    'E-Posta',
    'SSL',
    'Yazilim Pratikleri',
]

SSO_PROVIDER_MAP = {
    'google': {
        'label': 'Google',
        'login_path': '/accounts/google/login/',
    },
    'facebook': {
        'label': 'Facebook',
        'login_path': '/accounts/facebook/login/',
    },
    'linkedin': {
        'label': 'LinkedIn',
        'login_path': '/accounts/oidc/linkedin/login/',
    },
    'twitter': {
        'label': 'X / Twitter',
        'login_path': '/accounts/twitter_oauth2/login/',
    },
}


def get_sso_state():
    return {
        'google': bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET),
        'facebook': bool(settings.FACEBOOK_CLIENT_ID and settings.FACEBOOK_CLIENT_SECRET),
        'linkedin': bool(settings.LINKEDIN_CLIENT_ID and settings.LINKEDIN_CLIENT_SECRET),
        'twitter': bool(settings.TWITTER_CLIENT_ID and settings.TWITTER_CLIENT_SECRET),
    }


def get_knowledgebase_context():
    return {
        'knowledgebase_articles': KNOWLEDGEBASE_ARTICLES,
        'knowledgebase_trending': KNOWLEDGEBASE_ARTICLES[:4],
        'knowledgebase_categories': KNOWLEDGEBASE_CATEGORIES,
    }


def get_article_or_default(slug=None):
    if not slug:
        return KNOWLEDGEBASE_ARTICLES[0]

    for article in KNOWLEDGEBASE_ARTICLES:
        if article['slug'] == slug:
            return article

    raise Http404('Article not found')


def indexSix(request):
    context = {
        'page_title': 'QyberHost Django - Home',
    }
    return render(request, 'index-six.html', context)


def about(request):
    context = {
        'page_title': 'QyberHost Django - About',
    }
    return render(request, 'about.html', context)


def pricing(request):
    context = {
        'page_title': 'QyberHost Django - Pricing',
    }
    return render(request, 'pricing.html', context)


def affiliate(request):
    context = {
        'page_title': 'QyberHost Django - Affiliate',
    }
    return render(request, 'affiliate.html', context)


def signUp(request):
    form = SignUpForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        profile = user.profile
        profile.role = form.cleaned_data['role']
        profile.company_name = form.cleaned_data['company_name'].strip()
        profile.phone = form.cleaned_data['phone'].strip()
        profile.save()

        login(request, user)
        messages.success(request, 'Hesabiniz basariyla olusturuldu.')
        return redirect(settings.LOGIN_REDIRECT_URL)

    context = {
        'page_title': 'QyberHost Django - Sign Up',
        'form': form,
        'public_role_choices': UserProfile.PUBLIC_ROLE_CHOICES,
        'sso_state': get_sso_state(),
    }
    return render(request, 'auth/sign-up.html', context)


def partner(request):
    context = {
        'page_title': 'QyberHost Django - Partner',
    }
    return render(request, 'partner.html', context)


def support(request):
    context = {
        'page_title': 'QyberHost Django - Support',
    }
    return render(request, 'support.html', context)


def pricingTwo(request):
    context = {
        'page_title': 'QyberHost Django - Pricing Two',
    }
    return render(request, 'pricing-two.html', context)


def businessMail(request):
    context = {
        'page_title': 'QyberHost Django - Business Mail',
    }
    return render(request, 'business-mail.html', context)


def signIn(request):
    form = SignInForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )

        if user is None:
            form.add_error(None, 'Kullanici adi veya sifre hatali.')
        else:
            login(request, user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            messages.success(request, 'Giris basarili.')
            return redirect(settings.LOGIN_REDIRECT_URL)

    context = {
        'page_title': 'QyberHost Django - Sign In',
        'form': form,
        'sso_state': get_sso_state(),
    }
    return render(request, 'auth/sign-in.html', context)


def startSocialLogin(request, provider):
    sso_state = get_sso_state()
    provider_config = SSO_PROVIDER_MAP.get(provider)

    if provider_config is None:
        messages.error(request, 'Desteklenmeyen SSO saglayicisi.')
        return redirect('sign-in')

    if not sso_state.get(provider):
        messages.warning(request, f"{provider_config['label']} SSO ayarlari henuz tamamlanmadi.")
        return redirect('sign-in')

    selected_role = request.GET.get('role')
    if selected_role in dict(UserProfile.PUBLIC_ROLE_CHOICES):
        request.session['pending_social_role'] = selected_role
    else:
        request.session.pop('pending_social_role', None)

    login_path = provider_config['login_path']
    if request.user.is_authenticated:
        separator = '&' if '?' in login_path else '?'
        login_path = f"{login_path}{separator}process=connect"

    return redirect(login_path)


def forgotPassword(request):
    context = {
        'page_title': 'QyberHost Django - Forgot Password',
    }
    return render(request, 'auth/forgot-password.html', context)


def maintenance(request):
    context = {
        'page_title': 'QyberHost Django - Maintenance',
    }
    return render(request, 'errors/maintenance-service/maintenance.html', context)


def domainChecker(request):
    context = {
        'page_title': 'QyberHost Django - Domain Checker',
    }
    return render(request, 'domain-checker.html', context)


def pricingThree(request):
    context = {
        'page_title': 'QyberHost Django - Pricing Three',
    }
    return render(request, 'pricing-three.html', context)


def sslCertificate(request):
    context = {
        'page_title': 'QyberHost Django - SSL Certificate',
    }
    return render(request, 'ssl-certificate.html', context)


def whois(request):
    context = {
        'page_title': 'QyberHost Django - Whois',
    }
    return render(request, 'whois.html', context)


def blogGrid(request):
    active_tag = request.GET.get('tag')
    active_category = request.GET.get('category')
    articles = KNOWLEDGEBASE_ARTICLES

    if active_tag:
        articles = [
            item for item in articles
            if active_tag in item['tags']
        ]

    if active_category:
        articles = [
            item for item in articles
            if item['category'] == active_category
        ]

    active_filter = active_tag or active_category
    context = {
        'page_title': 'QyberHost Django - Knowledgebase Categories',
        'articles': articles,
        'active_filter': active_filter,
        'active_filter_type': 'etiket' if active_tag else 'kategori' if active_category else '',
    }
    context.update(get_knowledgebase_context())
    return render(request, 'blog-grid-2.html', context)


def blackFriday(request):
    context = {
        'page_title': 'QyberHost Django - Black Friday',
    }
    return render(request, 'black-friday.html', context)


def contact(request):
    context = {
        'page_title': 'QyberHost Django - Contact',
    }
    return render(request, 'contact.html', context)


def paymentMethod(request):
    context = {
        'page_title': 'QyberHost Django - Payment Method',
    }
    return render(request, 'payment-method.html', context)


def domainTransfer(request):
    context = {
        'page_title': 'QyberHost Django - Domain Transfer',
    }
    return render(request, 'domain-transfer.html', context)


def knowledgebase(request):
    context = {
        'page_title': 'QyberHost Django - Knowledgebase',
    }
    context.update(get_knowledgebase_context())
    return render(request, 'knowledgebase.html', context)


def blogDetails(request, slug=None):
    article = get_article_or_default(slug)
    related_articles = [item for item in KNOWLEDGEBASE_ARTICLES if item['slug'] != article['slug']][:4]
    context = {
        'page_title': f"QyberHost Django - {article['title']}",
        'article': article,
        'related_articles': related_articles,
    }
    context.update(get_knowledgebase_context())
    return render(request, 'blog-details.html', context)


def error(request):
    context = {
        'page_title': 'QyberHost Django - Error',
    }
    return render(request, 'errors/http-status/404.html', context)


def sharedHosting(request):
    context = {
        'page_title': 'QyberHost Django - Shared Hosting',
    }
    return render(request, 'shared-hosting.html', context)


def wordpressHosting(request):
    context = {
        'page_title': 'QyberHost Django - WordPress Hosting',
    }
    return render(request, 'wordpress-hosting.html', context)


def vpsHosting(request):
    context = {
        'page_title': 'QyberHost Django - VPS Hosting',
    }
    return render(request, 'vps-hosting.html', context)


def resellerHosting(request):
    context = {
        'page_title': 'QyberHost Django - Reseller Hosting',
    }
    return render(request, 'reseller-hosting.html', context)


def dedicatedHosting(request):
    context = {
        'page_title': 'QyberHost Django - Dedicated Hosting',
    }
    return render(request, 'dedicated-hosting.html', context)


def cloudHosting(request):
    context = {
        'page_title': 'QyberHost Django - Cloud Hosting',
    }
    return render(request, 'cloud-hosting.html', context)


def domainRegistration(request):
    context = {
        'page_title': 'QyberHost Django - Domain Registration',
    }
    return render(request, 'domain-registration.html', context)


def technology(request):
    context = {
        'page_title': 'QyberHost Django - Technology',
    }
    return render(request, 'technology.html', context)


def dataCenter(request):
    context = {
        'page_title': 'QyberHost Django - Data Center',
    }
    return render(request, 'data-center.html', context)


def gameDetails(request):
    context = {
        'page_title': 'QyberHost Django - Game Details',
    }
    return render(request, 'game-details.html', context)


def faq(request):
    context = {
        'page_title': 'QyberHost Django - FAQ',
    }
    return render(request, 'faq.html', context)


def adsBannerOne(request):
    context = {
        'page_title': 'QyberHost Django - Ads Banner One',
    }
    return render(request, 'hosting-offer-one.html', context)


def tos(request):
    context = {
        'page_title': 'QyberHost Django - Terms of Service',
    }
    return render(request, 'tos.html', context)


def privacy(request):
    context = {
        'page_title': 'QyberHost Django - Privacy Policy',
    }
    return render(request, 'privacy.html', context)


def cookies(request):
    context = {
        'page_title': 'QyberHost Django - Cookies Policy',
    }
    return render(request, 'cookies.html', context)
