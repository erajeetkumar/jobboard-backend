from django.test import TestCase

# Create test cases for the models
from companies.models import Company, Industry, CompanyMember
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.permissions import IsEmployerAndMember

User = get_user_model()
class IndustryModelTest(TestCase):
    def setUp(self):
        self.industry = Industry.objects.create(name="Tech", description="Technology sector")

    def test_industry_str(self):
        self.assertEqual(str(self.industry), "Tech")
    def test_industry_creation(self):   
        industry = Industry.objects.create(name="Finance", description="Financial sector")
        self.assertEqual(industry.name, "Finance")
        self.assertEqual(industry.description, "Financial sector")
        self.assertIsInstance(industry, Industry)
    def test_industry_unique_name(self):
        Industry.objects.create(name="Healthcare", description="Health sector")
        with self.assertRaises(Exception):
            Industry.objects.create(name="Healthcare", description="Duplicate name")
    def test_industry_description_blank(self):
        industry = Industry.objects.create(name="Education", description="")
        self.assertEqual(industry.description, "")
    def test_industry_description_not_blank(self):
        industry = Industry.objects.create(name="Education", description="Educational sector")
        self.assertNotEqual(industry.description, "")
    def test_industry_name_max_length(self):
        industry = Industry.objects.create(name="A" * 151, description="Long name test")
        self.assertTrue(len(industry.name) <= 150)
    def test_industry_description_max_length(self):
        industry = Industry.objects.create(name="Short", description="A" * 1001)
        self.assertTrue(len(industry.description) <= 1000)
    def test_industry_creation_with_blank_description(self):
        industry = Industry.objects.create(name="Retail", description="")
        self.assertEqual(industry.description, "")
    def test_industry_creation_with_long_description(self):
        industry = Industry.objects.create(name="Retail", description="A" * 1001)
        self.assertTrue(len(industry.description) <= 1000)
    def test_industry_creation_with_special_characters(self):
        industry = Industry.objects.create(name="Retail@2023", description="Special characters test")
        self.assertEqual(industry.name, "Retail@2023")
        self.assertEqual(industry.description, "Special characters test")
    def test_industry_creation_with_numeric_name(self):
        industry = Industry.objects.create(name="12345", description="Numeric name test")
        self.assertEqual(industry.name, "12345")
        self.assertEqual(industry.description, "Numeric name test")
    def test_industry_creation_with_blank_name(self):
        with self.assertRaises(Exception):
            Industry.objects.create(name="", description="Blank name test")


class CompanyModelTest(TestCase):
    def setUp(self):
        self.industry = Industry.objects.create(name="Tech", description="Technology sector")
        self.company = Company.objects.create(
            name="Tech Corp",
            website="http://techcorp.com",
            industry=self.industry,
            location="New York",
            description="A tech company",
            established_year=2000,
            is_verified=True,
            is_active=True
        )
    def test_company_str(self):
        self.assertEqual(str(self.company), "Tech Corp")
    def test_company_creation(self):
        company = Company.objects.create(
            name="Finance Inc",
            website="http://financeinc.com",
            industry=self.industry,
            location="San Francisco",
            description="A finance company",
            established_year=1995,
            is_verified=False,
            is_active=True
        )
        self.assertEqual(company.name, "Finance Inc")
        self.assertEqual(company.website, "http://financeinc.com")
        self.assertEqual(company.industry, self.industry)
        self.assertEqual(company.location, "San Francisco")
        self.assertEqual(company.description, "A finance company")
        self.assertEqual(company.established_year, 1995)
        self.assertFalse(company.is_verified)
        self.assertTrue(company.is_active)
    def test_company_unique_name(self):
        Company.objects.create(
            name="Retail LLC",
            website="http://retail.com",
            industry=self.industry,
            location="Los Angeles",
            description="A retail company",
            established_year=2010,
            is_verified=True,
            is_active=True
        )
        with self.assertRaises(Exception):
            Company.objects.create(
                name="Retail LLC",
                website="http://duplicate.com",
                industry=self.industry,
                location="Chicago",
                description="Duplicate name test",
                established_year=2015,
                is_verified=False,
                is_active=True
            )
    def test_company_website_blank(self):
        company = Company.objects.create(
            name="Tech Solutions",
            website="",
            industry=self.industry,
            location="Austin",
            description="A tech solutions company",
            established_year=2015,
            is_verified=True,
            is_active=True
        )
        self.assertEqual(company.website, "")
    def test_company_website_not_blank(self):
        company = Company.objects.create(
            name="Tech Solutions",
            website="http://techsolutions.com",
            industry=self.industry,
            location="Austin",
            description="A tech solutions company",
            established_year=2015,
            is_verified=True,
            is_active=True
        )
        self.assertNotEqual(company.website, "")
    def test_company_location_blank(self):
        company = Company.objects.create(
            name="Tech Innovations",
            website="http://techinnovations.com",
            industry=self.industry,
            location="",
            description="A tech innovations company",
            established_year=2020,
            is_verified=True,
            is_active=True
        )
        self.assertEqual(company.location, "")
    
    def test_company_slug_creation(self):
        company = Company.objects.create(
            name="Tech Innovations",
            website="http://techinnovations.com",
            industry=self.industry,
            location="Austin",
            description="A tech innovations company",
            established_year=2020,
            is_verified=True,
            is_active=True
        )
        self.assertEqual(company.slug, "tech-innovations")