from django.shortcuts import redirect, render

from .views import require_account_permission, require_active_membership


RECEIPT_DEMO_ROWS = [
    {"id": 105480, "created": "18/03/2026", "due": "02/04/2026", "amount": "661,66TL", "status": "cancelled", "status_label": "Iptal Edildi", "invoice_ready": False},
    {"id": 103813, "created": "08/02/2026", "due": "23/02/2026", "amount": "90,00TL", "status": "paid", "status_label": "Odendi", "invoice_ready": False},
    {"id": 103888, "created": "10/02/2026", "due": "13/02/2026", "amount": "150,00TL", "status": "paid", "status_label": "Odendi", "invoice_ready": True},
    {"id": 97326, "created": "17/09/2025", "due": "20/09/2025", "amount": "200,00TL", "status": "refunded", "status_label": "Iade Edildi", "invoice_ready": False},
    {"id": 96230, "created": "22/08/2025", "due": "25/08/2025", "amount": "50,00TL", "status": "refunded", "status_label": "Iade Edildi", "invoice_ready": True},
    {"id": 96229, "created": "22/08/2025", "due": "25/08/2025", "amount": "300,00TL", "status": "paid", "status_label": "Odendi", "invoice_ready": True},
    {"id": 91748, "created": "17/04/2025", "due": "02/05/2025", "amount": "6.876,60TL", "status": "paid", "status_label": "Odendi", "invoice_ready": True},
    {"id": 90815, "created": "22/03/2025", "due": "06/04/2025", "amount": "1.589,21TL", "status": "paid", "status_label": "Odendi", "invoice_ready": True},
]

EMAIL_HISTORY_DEMO_ROWS = [
    {"sent_at": "30/04/2026 (22:26)", "subject": "[Bilgilendirme] Kuresel cPanel Guvenlik Zafiyeti (CVE-2026-41940) ve Alinan Onlemler"},
    {"sent_at": "09/04/2026 (11:00)", "subject": "Hizmetiniz durduruldu!"},
    {"sent_at": "03/04/2026 (10:01)", "subject": "Domain Tescil Sureniz Gecti!"},
    {"sent_at": "02/04/2026 (16:39)", "subject": "[Ticket ID: DH-V7V40] ERISIM BILGILERI"},
    {"sent_at": "31/03/2026 (10:02)", "subject": "Domain Yenileme Sureniz Yaklasiyor"},
    {"sent_at": "31/03/2026 (10:00)", "subject": "Urun/Hizmet icin Bekleyen Odeme"},
    {"sent_at": "23/03/2026 (10:01)", "subject": "Domain Yenileme Sureniz Yaklasiyor"},
    {"sent_at": "18/03/2026 (10:00)", "subject": "Yeni Hizmet Makbuzunuz #105480"},
    {"sent_at": "05/03/2026 (20:37)", "subject": "[Ticket ID: DH-H7T51] Booking Balkans"},
    {"sent_at": "03/03/2026 (10:04)", "subject": "Domain Yenileme Sureniz Yaklasiyor"},
]

SUPPORT_DEPARTMENTS = [
    {
        "slug": "technical",
        "name": "Teknik Destek",
        "description": "Tum hizmetler icin teknik yardim departmani",
        "deptid": 3,
    },
    {
        "slug": "billing",
        "name": "Satis/Muhasebe Destek",
        "description": "Muhasebesel isler (fatura vb) yardim departmani",
        "deptid": 5,
    },
    {
        "slug": "payment",
        "name": "Odeme Bildirimi",
        "description": "Havale ve EFT bildirimlerinizi bu bolumden bize ulastirabilirsiniz",
        "deptid": 2,
    },
]

RECENT_TICKETS = [
    {"id": "DH-V7V40", "subject": "ERISIM BILGILERI", "age": "3 hafta once", "status": "Kapandi"},
    {"id": "DH-H7T51", "subject": "Booking Balkans", "age": "1 ay once", "status": "Kapandi"},
    {"id": "DH-G4H15", "subject": "Email Hakkinda", "age": "1 ay once", "status": "Kapandi"},
    {"id": "DH-A7J94", "subject": "Email Hakkinda", "age": "2 ay once", "status": "Kapandi"},
    {"id": "DH-J0N45", "subject": "samad.mk domaini hakkinda", "age": "3 ay once", "status": "Kapandi"},
]

SUPPORT_TICKETS = [
    {"department": "Teknik Destek", "ticket_id": "DH-V7V40", "subject": "ERISIM BILGILERI", "status": "Kapandi", "updated_at": "09/04/2026 (18:00)"},
    {"department": "Teknik Destek", "ticket_id": "DH-H7T51", "subject": "Booking Balkans", "status": "Kapandi", "updated_at": "12/03/2026 (20:55)"},
    {"department": "Teknik Destek", "ticket_id": "DH-G4H15", "subject": "Email Hakkinda", "status": "Kapandi", "updated_at": "12/03/2026 (17:40)"},
    {"department": "Teknik Destek", "ticket_id": "DH-A7J94", "subject": "Email Hakkinda", "status": "Kapandi", "updated_at": "26/02/2026 (18:25)"},
    {"department": "Teknik Destek", "ticket_id": "DH-J0N45", "subject": "samad.mk domaini hakkinda", "status": "Kapandi", "updated_at": "06/01/2026 (17:55)"},
    {"department": "Alan Adi Belge Yonetimi", "ticket_id": "DH-B6N94", "subject": "Belge Talebi: balkantatili.com.tr", "status": "Kapandi", "updated_at": "12/10/2025 (00:40)"},
]

ANNOUNCEMENT_MONTHS = [
    "Mar 2026",
    "Eki 2025",
    "Eyl 2025",
    "Oca 2025",
    "Kas 2024",
    "Tem 2024",
    "May 2024",
    "Oca 2024",
]

ANNOUNCEMENTS = [
    {
        "title": "PHP 8.4 ve 8.5 Destegi Aktif Edildi",
        "summary": "CloudLinux altyapimizda PHP 8.4 ve 8.5 surumleri tum Linux sunucularimizda aktif edildi.",
        "date": "17 Mar 2026",
    },
    {
        "title": "cPanel Ucretsiz SSL Sisteminde Yenilik: AutoSSL'e Gecis",
        "summary": "FleetSSL kaldirilarak cPanel yerlesik AutoSSL sistemine gecis tamamlandi.",
        "date": "14 Eki 2025",
    },
    {
        "title": "Yeni Ozellik: Geri Bildirimler Dogrudan Ekip Liderine Ulasiyor",
        "summary": "Destek merkezinden iletilen memnuniyet, oneri ve sikayetler dogrudan ekip liderine aktariliyor.",
        "date": "05 Eyl 2025",
    },
    {
        "title": "%20 Erken Yenileme Indirim Firsati",
        "summary": "Web hosting ve bulut sunucu hizmetlerinde erken yenileme icin kampanya duyurusu.",
        "date": "13 Oca 2025",
    },
]

RELATED_SERVICES = [
    "Eco Mail 1 - kompas.com.mk (Durduruldu)",
    "SSD VDS Bulut Sunucu - vds.94575.domainhizmetleri.com (Aktif)",
    "Domain - balkangezisi.com.tr (Aktif)",
    "Domain - balkanseyahati.com.tr (Aktif)",
    "Domain - balkantura.com.tr (Aktif)",
    "Domain - bookingbalkans.com (Kurtarma Donemi)",
    "Domain - cityrealestate.com.tr (Aktif)",
    "Domain - dancepanel.com.tr (Aktif)",
    "Domain - dancestudio.com.tr (Aktif)",
    "Domain - dansokulucrm.com.tr (Aktif)",
    "Domain - qtechnology.com.tr (Aktif)",
]


@require_active_membership
def index(request):
    membership = request.active_membership
    context={
        "page_title":"Musteri Paneli",
        "wallet_sidebar":"active",
        "active_account": request.active_account,
        "active_membership": membership,
        "permissions": {
            "billing": membership.can_manage_billing,
            "technical": membership.can_manage_technical,
            "users": membership.can_manage_users,
            "affiliate": membership.can_manage_affiliate,
            "tickets": membership.can_open_tickets,
        },
    }
    return render(request,'nexadash/customer/dashboard.html',context)

def crm(request):
    context={
        "page_title":"CRM",
        "wallet_sidebar":""
    }
    return render(request,'nexadash/crm.html',context)

def finance(request):
    context={
        "page_title":"Finance",
        "wallet_sidebar":""
    }
    return render(request,'nexadash/finance.html',context)
	
def analytics(request):
    context={
        "page_title":"Analytics",
        "wallet_sidebar":"active"
    }
    return render(request,'nexadash/analytics.html',context)
	
def sales(request):
    context={
        "page_title":"Sales",
        "wallet_sidebar":""
    }
    return render(request,'nexadash/sales.html',context)
    
def ecommerce(request):
    context={
        "page_title":"Ecommerce",
        "wallet_sidebar":""
    }
    return render(request,'nexadash/ecommerce.html',context)
    
def course(request):
    context={
        "page_title":"Course",
        "wallet_sidebar":""
    }
    return render(request,'nexadash/course.html',context)
    
def medical(request):
    context={
        "page_title":"Medical",
        "wallet_sidebar":""
    }
    return render(request,'nexadash/medical.html',context)


    
def overview(request):
    context={
        "page_title":"Overview"
    }
    return render(request,'nexadash/profile/overview.html',context)

def projects(request):
    context={
        "page_title":"Projects"
    }
    return render(request,'nexadash/profile/projects.html',context)

def projects_details(request):
    context={
        "page_title":"Projects Details"
    }
    return render(request,'nexadash/profile/projects-details.html',context)

def campaigns(request):
    context={
        "page_title":"Campaigns"
    }
    return render(request,'nexadash/profile/campaigns.html',context)

def documents(request):
    context={
        "page_title":"Documents"
    }
    return render(request,'nexadash/profile/documents.html',context)

def followers(request):
    context={
        "page_title":"Followers"
    }
    return render(request,'nexadash/profile/followers.html',context)

def activity(request):
    context={
        "page_title":"Activity"
    }
    return render(request,'nexadash/profile/activity.html',context)

def account_overview(request):
    context={
        "page_title":"Account Overview"
    }
    return render(request,'nexadash/account/overview.html',context)

def account_settings(request):
    context={
        "page_title":"Account Settings"
    }
    return render(request,'nexadash/account/settings.html',context)

@require_active_membership
def account_security(request):
    context={
        "page_title":"Hesap Guvenligi"
    }
    return render(request,'nexadash/account/security.html',context)

def account_activity(request):
    context={
        "page_title":"Account Activity"
    }
    return render(request,'nexadash/account/activity.html',context)

@require_account_permission("billing")
def billing(request):
    return redirect("nexadash:statements")

@require_account_permission("billing")
def statements(request):
    paid_count = len([r for r in RECEIPT_DEMO_ROWS if r["status"] == "paid"])
    unpaid_count = len([r for r in RECEIPT_DEMO_ROWS if r["status"] == "unpaid"])
    cancelled_count = len([r for r in RECEIPT_DEMO_ROWS if r["status"] == "cancelled"])
    refunded_count = len([r for r in RECEIPT_DEMO_ROWS if r["status"] == "refunded"])
    context={
        "page_title":"Makbuzlarim",
        "receipts": RECEIPT_DEMO_ROWS,
        "receipt_stats": {
            "paid": paid_count,
            "unpaid": unpaid_count,
            "cancelled": cancelled_count,
            "refunded": refunded_count,
        }
    }
    return render(request,'nexadash/account/statements.html',context)


@require_account_permission("billing")
def receipt_invoice(request, receipt_id):
    receipt = next((r for r in RECEIPT_DEMO_ROWS if r["id"] == receipt_id), None)
    if receipt is None:
        return redirect("nexadash:statements")

    context = {
        "page_title": f"E-Fatura #{receipt_id}",
        "receipt": receipt,
    }
    return render(request, "nexadash/account/receipt-invoice.html", context)


@require_account_permission("billing")
def add_funds(request):
    context = {
        "page_title": "Bakiye Yukle",
        "balance": "0.00 TL",
        "min_amount": "50,00TL",
        "max_amount": "500.000,00TL",
        "max_total_balance": "1.000.000,00TL",
        "payment_methods": [
            "Kredi Karti (3D Secure)",
            "KuveytTurk Havale/EFT",
            "Ziraat Bankasi Havale/EFT",
            "YapiKredi Bankasi Havale/EFT",
            "Enpara Havale/EFT",
        ],
    }
    return render(request, "nexadash/account/add-funds.html", context)


@require_active_membership
def payment_methods(request):
    context = {
        "page_title": "Kayitli Kredi Kartlarim",
        "cards": [],
    }
    return render(request, "nexadash/account/payment-methods.html", context)


@require_active_membership
def payment_method_add(request):
    context = {
        "page_title": "Yeni Kredi Karti Ekle",
    }
    return render(request, "nexadash/account/payment-method-add.html", context)


@require_account_permission("users")
def user_management(request):
    context = {
        "page_title": "Hesap Yetkilisi Yonetimi",
        "user_count": 1,
        "users": [
            {
                "email": "volkandortkardes@qtechnology.com.mk",
                "is_owner": True,
                "two_fa_enabled": False,
                "last_login": "2 saat once",
            }
        ],
    }
    return render(request, "nexadash/account/user-management.html", context)


@require_account_permission("users")
def contacts(request):
    context = {
        "page_title": "Bildirim Kisileri",
        "contacts": [
            {
                "id": 2540,
                "full_name": "Fatih Kuroglu",
                "email": "info@ahenkerp.com",
                "company": "AHENK ERP",
                "phone": "+90 552 463 46 50",
                "address1": "BURSA",
                "address2": "BURSA",
                "city": "BURSA",
                "state": "INEGOL",
                "postcode": "",
                "country": "Turkey",
            }
        ],
    }
    return render(request, "nexadash/account/contacts.html", context)


@require_active_membership
def email_history(request):
    context = {
        "page_title": "Eposta Gecmisi",
        "emails": EMAIL_HISTORY_DEMO_ROWS,
    }
    return render(request, "nexadash/account/email-history.html", context)


@require_account_permission("tickets")
def support_new_ticket(request):
    context = {
        "page_title": "Yeni Destek Talebi",
        "departments": SUPPORT_DEPARTMENTS,
        "recent_tickets": RECENT_TICKETS,
    }
    return render(request, "nexadash/support/new-ticket.html", context)


@require_account_permission("tickets")
def support_new_ticket_department(request, dept_slug):
    department = next((d for d in SUPPORT_DEPARTMENTS if d["slug"] == dept_slug), None)
    if department is None:
        return redirect("nexadash:support-new-ticket")

    context = {
        "page_title": "Yeni Destek Talebi",
        "department": department,
        "departments": SUPPORT_DEPARTMENTS,
        "recent_tickets": RECENT_TICKETS,
        "related_services": RELATED_SERVICES,
        "show_payment_fields": department["slug"] == "payment",
        "payment_banks": ["Ziraat Bankasi", "YapiKredi Bankasi", "Enpara", "KuveytTurk"],
    }
    return render(request, "nexadash/support/new-ticket-form.html", context)


@require_account_permission("tickets")
def support_tickets(request):
    status_counts = {
        "acik": 0,
        "yanitlandi": 0,
        "musteri_yanitladi": 0,
        "cevap_bekleniyor": 4,
        "kapandi": 254,
    }
    context = {
        "page_title": "Destek Kayitlarim",
        "tickets": SUPPORT_TICKETS,
        "status_counts": status_counts,
    }
    return render(request, "nexadash/support/tickets.html", context)


@require_active_membership
def support_announcements(request):
    context = {
        "page_title": "Duyurular ve Haberler",
        "months": ANNOUNCEMENT_MONTHS,
        "announcements": ANNOUNCEMENTS,
    }
    return render(request, "nexadash/support/announcements.html", context)

def referrals(request):
    context={
        "page_title":"Referrals"
    }
    return render(request,'nexadash/account/referrals.html',context)

def api_keys(request):
    context={
        "page_title":"Api Keys"
    }
    return render(request,'nexadash/account/api-keys.html',context)

def logs(request):
    context={
        "page_title":"Logs"
    }
    return render(request,'nexadash/account/logs.html',context)

def auto_write(request):
    context={
        "page_title":"Auto Write"
    }
    return render(request,'nexadash/aikit/auto-write.html',context)

def chatbot(request):
    context={
        "page_title":"Chat Bot"
    }
    return render(request,'nexadash/aikit/chatbot.html',context)

def fine_tune_models(request):
    context={
        "page_title":"Fine Tune Models"
    }
    return render(request,'nexadash/aikit/fine-tune-models.html',context)

def imports(request):
    context={
        "page_title":"Import"
    }
    return render(request,'nexadash/aikit/import.html',context)

def prompt(request):
    context={
        "page_title":"Prompt"
    }
    return render(request,'nexadash/aikit/prompt.html',context)

def repurpose(request):
    context={
        "page_title":"Repurpose"
    }
    return render(request,'nexadash/aikit/repurpose.html',context)

def rss(request):
    context={
        "page_title":"RSS"
    }
    return render(request,'nexadash/aikit/rss.html',context)

def scheduled(request):
    context={
        "page_title":"Scheduled"
    }
    return render(request,'nexadash/aikit/scheduled.html',context)

def setting(request):
    context={
        "page_title":"Setting"
    }
    return render(request,'nexadash/aikit/setting.html',context)

def content(request):
    context={
        "page_title":"Content"
    }
    return render(request,'nexadash/cms/content.html',context)

def add_content(request):
    context={
        "page_title":"Add Content"
    }
    return render(request,'nexadash/cms/add-content.html',context)

def menu(request):
    context={
        "page_title":"Menu"
    }
    return render(request,'nexadash/cms/menu.html',context)

def email_template(request):
    context={
        "page_title":"Email Template"
    }
    return render(request,'nexadash/cms/email-template.html',context)

def add_email(request):
    context={
        "page_title":"Add Email"
    }
    return render(request,'nexadash/cms/add-email.html',context)

def blog(request):
    context={
        "page_title":"Blog"
    }
    return render(request,'nexadash/cms/blog.html',context)

def add_blog(request):
    context={
        "page_title":"Add Blog"
    }
    return render(request,'nexadash/cms/add-blog.html',context)

def blog_category(request):
    context={
        "page_title":"Blog Category"
    }
    return render(request,'nexadash/cms/blog-category.html',context)

def chat(request):
    context={
        "page_title":"Chat"
    }
    return render(request,'nexadash/apps/user/chat.html',context)

def app_profile_1(request):
    context={
        "page_title":"Profile 1"
    }
    return render(request,'nexadash/apps/user/app-profile-1.html',context)

def app_profile_2(request):
    context={
        "page_title":"Profile 2"
    }
    return render(request,'nexadash/apps/user/app-profile-2.html',context)

def edit_profile(request):
    context={
        "page_title":"Edit Profile"
    }
    return render(request,'nexadash/apps/user/edit-profile.html',context)

def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'nexadash/apps/user/post-details.html',context)


def email_compose(request):
    context={
        "page_title":"Compose"
    }
    return render(request,'nexadash/apps/email/email-compose.html',context)


def email_inbox(request):
    context={
        "page_title":"Inbox"
    }
    return render(request,'nexadash/apps/email/email-inbox.html',context)


def email_read(request):
    context={
        "page_title":"Read"
    }
    return render(request,'nexadash/apps/email/email-read.html',context)


def app_calendar(request):
    context={
        "page_title":"App Calendar"
    }
    return render(request,'nexadash/ecommerce/app-calendar.html',context)


def category_table(request):
    context={
        "page_title":"Category Table"
    }
    return render(request,'nexadash/ecommerce/category/category-table.html',context)

def add_category(request):
    context={
        "page_title":"Add Category"
    }
    return render(request,'nexadash/ecommerce/category/add-category.html',context)

def edit_category(request):
    context={
        "page_title":"Edit Category"
    }
    return render(request,'nexadash/ecommerce/category/edit-category.html',context)

def product_table(request):
    context={
        "page_title":"Product Table"
    }
    return render(request,'nexadash/ecommerce/product/product-table.html',context)

def add_product(request):
    context={
        "page_title":"Add Product"
    }
    return render(request,'nexadash/ecommerce/product/add-product.html',context)

def edit_product(request):
    context={
        "page_title":"Edit Product"
    }
    return render(request,'nexadash/ecommerce/product/edit-product.html',context)


def ecom_product_grid(request):
    context={
        "page_title":"Product Grid"
    }
    return render(request,'nexadash/ecommerce/shop/ecom-product-grid.html',context)


def ecom_product_list(request):
    context={
        "page_title":"Product List"
    }
    return render(request,'nexadash/ecommerce/shop/ecom-product-list.html',context)


def ecom_product_detail(request):
    context={
        "page_title":"Product Detail"
    }
    return render(request,'nexadash/ecommerce/shop/ecom-product-detail.html',context)


def ecom_product_order(request):
    context={
        "page_title":"Product Order"
    }
    return render(request,'nexadash/ecommerce/shop/ecom-product-order.html',context)


def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'nexadash/ecommerce/shop/ecom-checkout.html',context)


def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'nexadash/ecommerce/shop/ecom-invoice.html',context)


def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'nexadash/ecommerce/shop/ecom-customers.html',context)


def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'nexadash/bootstrap/ui-accordion.html',context)


def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'nexadash/bootstrap/ui-alert.html',context)


def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'nexadash/bootstrap/ui-badge.html',context)


def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'nexadash/bootstrap/ui-button.html',context)


def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'nexadash/bootstrap/ui-modal.html',context)


def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'nexadash/bootstrap/ui-button-group.html',context)


def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'nexadash/bootstrap/ui-list-group.html',context)


def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'nexadash/bootstrap/ui-card.html',context)


def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'nexadash/bootstrap/ui-carousel.html',context)


def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'nexadash/bootstrap/ui-dropdown.html',context)


def ui_offcanvas(request):
    context={
        "page_title":"Offcanvas"
    }
    return render(request,'nexadash/bootstrap/ui-offcanvas.html',context)


def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'nexadash/bootstrap/ui-popover.html',context)


def ui_breadcrumb(request):
    context={
        "page_title":"Breadcrumb"
    }
    return render(request,'nexadash/bootstrap/ui-breadcrumb.html',context)


def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'nexadash/bootstrap/ui-progressbar.html',context)


def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'nexadash/bootstrap/ui-tab.html',context)


def ui_media_object(request):
    context={
        "page_title":"Media Object"
    }
    return render(request,'nexadash/bootstrap/ui-media-object.html',context)


def ui_toasts(request):
    context={
        "page_title":"Toasts"
    }
    return render(request,'nexadash/bootstrap/ui-toasts.html',context)


def ui_spinners(request):
    context={
        "page_title":"Spinners"
    }
    return render(request,'nexadash/bootstrap/ui-spinners.html',context)


def ui_scrollspy(request):
    context={
        "page_title":"Scrollspy"
    }
    return render(request,'nexadash/bootstrap/ui-scrollspy.html',context)


def ui_range_slider(request):
    context={
        "page_title":"Range Slider"
    }
    return render(request,'nexadash/bootstrap/ui-range-slider.html',context)


def ui_placeholder(request):
    context={
        "page_title":"Placeholder"
    }
    return render(request,'nexadash/bootstrap/ui-placeholder.html',context)


def ui_object_fit(request):
    context={
        "page_title":"Object Fit"
    }
    return render(request,'nexadash/bootstrap/ui-object-fit.html',context)


def ui_colors(request):
    context={
        "page_title":"Colors"
    }
    return render(request,'nexadash/bootstrap/ui-colors.html',context)


def ui_navbar(request):
    context={
        "page_title":"Navbar"
    }
    return render(request,'nexadash/bootstrap/ui-navbar.html',context)


def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'nexadash/bootstrap/ui-typography.html',context)


def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'nexadash/bootstrap/ui-pagination.html',context)


def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'nexadash/bootstrap/ui-grid.html',context)



def chart_flot(request):
    context={
        "page_title":"Chart Flot"
    }
    return render(request,'nexadash/charts/chart-flot.html',context)


def chart_morris(request):
    context={
        "page_title":"Chart Morris"
    }
    return render(request,'nexadash/charts/chart-morris.html',context)


def chart_chartjs(request):
    context={
        "page_title":"Chart Chartjs"
    }
    return render(request,'nexadash/charts/chart-chartjs.html',context)


def chart_chartist(request):
    context={
        "page_title":"Chart Chartist"
    }
    return render(request,'nexadash/charts/chart-chartist.html',context)


def chart_sparkline(request):
    context={
        "page_title":"Chart Sparkline"
    }
    return render(request,'nexadash/charts/chart-sparkline.html',context)


def chart_peity(request):
    context={
        "page_title":"Chart Peity"
    }
    return render(request,'nexadash/charts/chart-peity.html',context)


def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'nexadash/plugins/uc-select2.html',context)


def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'nexadash/plugins/uc-nestable.html',context)


def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'nexadash/plugins/uc-noui-slider.html',context)


def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'nexadash/plugins/uc-sweetalert.html',context)


def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'nexadash/plugins/uc-toastr.html',context)

def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'nexadash/plugins/uc-lightgallery.html',context)

def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'nexadash/plugins/map-jqvmap.html',context)


def widget_basic(request):
    context={
        "page_title":"Widget"
    }
    return render(request,'nexadash/widget-basic.html',context)


def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'nexadash/forms/form-element.html',context)


def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'nexadash/forms/form-wizard.html',context)


def form_editor(request):
    context={
        "page_title":"CkEditor"
    }
    return render(request,'nexadash/forms/form-editor.html',context)


def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'nexadash/forms/form-pickers.html',context)


def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'nexadash/forms/form-validation.html',context)


def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'nexadash/table/table-bootstrap-basic.html',context)


def table_datatable_basic(request):
    context={
        "page_title":"Table Datatable"
    }
    return render(request,'nexadash/table/table-datatable-basic.html',context)


def page_empty(request):
    context={
        "page_title":"Empty Page"
    }
    return render(request,'nexadash/pages/page-empty.html',context)


def page_error_400(request):
    return render(request,'400.html')


def page_error_403(request):
    return render(request,'403.html')


def page_error_404(request):
    return render(request,'404.html')


def page_error_500(request):
    return render(request,'500.html')


def page_error_503(request):
    return render(request,'503.html')
    













