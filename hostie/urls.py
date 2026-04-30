"""
URL configuration for hostie_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hostie import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexSix, name='home'),
    path('index-six/', views.indexSix, name='index-six'),
    path('about/', views.about, name='about'),
    path('pricing/', views.pricing, name='pricing'),
    path('affiliate/', views.affiliate, name='affiliate'),
    path('sign-up/', views.signUp, name='sign-up'),
    path('blog/', views.blog, name='blog'),
    path('partner/', views.partner, name='partner'),
    path('support/', views.support, name='support'),
    path('pricing-two/', views.pricingTwo, name='pricing-two'),
    path('business-mail/', views.businessMail, name='business-mail'),
    path('sign-in/', views.signIn, name='sign-in'),
    path('blog-list/', views.blogList, name='blog-list'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('domain-checker/', views.domainChecker, name='domain-checker'),
    path('pricing-three/', views.pricingThree, name='pricing-three'),
    path('ssl-certificate/', views.sslCertificate, name='ssl-certificate'),
    path('whois/', views.whois, name='whois'),
    path('blog-grid-2/', views.blogGrid, name='blog-grid-2'),
    path('black-friday/', views.blackFriday, name='black-friday'),
    path('contact/', views.contact, name='contact'),
    path('payment-method/', views.paymentMethod, name='payment-method'),
    path('domain-transfer/', views.domainTransfer, name='domain-transfer'),
    path('knowledgebase/', views.knowledgebase, name='knowledgebase'),
    path('blog-details/', views.blogDetails, name='blog-details'),
    path('404/', views.error, name='404'),
    path('shared-hosting/', views.sharedHosting, name='shared-hosting'),
    path('wordpress-hosting/', views.wordpressHosting, name='wordpress-hosting'),
    path('vps-hosting/', views.vpsHosting, name='vps-hosting'),
    path('dedicated-hosting/', views.dedicatedHosting, name='dedicated-hosting'),
    path('cloud-hosting/', views.cloudHosting, name='cloud-hosting'),
    path('reseller-hosting/', views.resellerHosting, name='reseller-hosting'),
    path('domain-checker/', views.domainChecker, name='domain-checker'),
    path('domain-transfer/', views.domainTransfer, name='domain-transfer'),
    path('domain-registration/', views.domainRegistration, name='domain-registration'),
    path('technology/', views.technology, name='technology'),
    path('data-center/', views.dataCenter, name='data-center'),
    path('game-details/', views.gameDetails, name='game-details'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy-policy'),
    path('tos/', views.tos, name='tos'),
    path('cookies/', views.cookies, name='cookies'),
    path('hosting-offer-one/', views.adsBannerOne, name='hosting-offer-one'),
]
