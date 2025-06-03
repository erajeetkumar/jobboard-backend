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
        self.industry = Industry.objects.create(
            name="Tech", description="Technology sector"
        )

    def test_industry_str(self):
        self.assertEqual(str(self.industry), "Tech")

    def test_industry_creation(self):
        industry = Industry.objects.create(
            name="Finance", description="Financial sector"
        )
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
        industry = Industry.objects.create(
            name="Education", description="Educational sector"
        )
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
        industry = Industry.objects.create(
            name="Retail@2023", description="Special characters test"
        )
        self.assertEqual(industry.name, "Retail@2023")
        self.assertEqual(industry.description, "Special characters test")

    def test_industry_creation_with_numeric_name(self):
        industry = Industry.objects.create(
            name="12345", description="Numeric name test"
        )
        self.assertEqual(industry.name, "12345")
        self.assertEqual(industry.description, "Numeric name test")

    def test_industry_creation_with_blank_name(self):
        with self.assertRaises(Exception):
            Industry.objects.create(name="", description="Blank name test")


class CompanyModelTest(TestCase):
    def setUp(self):
        self.industry = Industry.objects.create(
            name="Tech", description="Technology sector"
        )
        self.company = Company.objects.create(
            name="Tech Corp",
            website="http://techcorp.com",
            industry=self.industry,
            location="New York",
            description="A tech company",
            established_year=2000,
            is_verified=True,
            is_active=True,
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
            is_active=True,
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
            is_active=True,
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
                is_active=True,
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
            is_active=True,
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
            is_active=True,
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
            is_active=True,
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
            is_active=True,
        )
        self.assertEqual(company.slug, "tech-innovations")


# create test cases for viewsets
from rest_framework_simplejwt.tokens import RefreshToken


class CompanyViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="employer@abc.com", password="password123", role="employer"
        )

        self.industry = Industry.objects.create(
            name="Tech", description="Technology sector"
        )
        self.company = Company.objects.create(
            name="Tech Corp",
            website="http://techcorp.com",
            industry=self.industry,
            location="New York",
            description="A tech company",
            established_year=2000,
            is_verified=True,
            is_active=True,
            created_by=self.user,
            logo=None,
        )
        self.create_url = reverse("company-list-create")
        self.delete_url = reverse("company-internal-detail", args=[self.company.id])
        self.company_member = CompanyMember.objects.create(
            user=self.user, company=self.company, role="admin"
        )
        self.company_member.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        # Set authorization header for all requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # create another user and add them to the company
        self.user2 = User.objects.create_user(
            email="recruiter@abc.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            role="recruiter",
        )
        self.company_member2 = CompanyMember.objects.create(
            user=self.user2, company=self.company, role="member"
        )
        self.company_member2.save()

        # create another employer user and create a new company
        self.user3 = User.objects.create_user(
            email="employer1@xyz.com",
            password="password123",
            role="employer",
            first_name="Jane",
            last_name="Smith",
        )
        self.company2 = Company.objects.create(
            name="Finance Inc",
            website="http://financeinc.com",
            industry=self.industry,
            location="San Francisco",
            description="A finance company",
            established_year=1995,
            is_verified=False,
            is_active=True,
            created_by=self.user3,
            logo=None,
        )
        self.company2_member = CompanyMember.objects.create(
            user=self.user3, company=self.company2, role="admin"
        )

        self.company2_member.save()

    def test_create_company(self):
        data = {
            "name": "New Company",
            "website": "http://newcompany.com",
            "industry": self.industry.id,
            "location": "Los Angeles",
            "description": "A new company",
            "established_year": 2023,
        }

        response = self.client.post(self.create_url, data)
        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 3)
        self.assertEqual(
            Company.objects.get(id=response.data["id"]).name, "New Company"
        )

    def test_create_company_without_authentication(self):
        self.client.logout()
        data = {
            "name": "New Company",
            "website": "http://newcompany.com",
            "industry": self.industry.id,
            "location": "Los Angeles",
            "description": "A new company",
            "established_year": 2023,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Company.objects.count(), 2)

    def test_create_company_with_invalid_data(self):
        data = {
            "name": "",
            "website": "invalid_url",
            "industry": self.industry.id,
            "location": "",
            "description": "A new company",
            "established_year": 2023,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 2)

    # test with different user roles
    def test_create_company_with_different_user_role(self):
        self.client.force_authenticate(user=self.user2)
        data = {
            "name": "New Company",
            "website": "http://newcompany.com",
            "industry": self.industry.id,
            "location": "Los Angeles",
            "description": "A new company",
            "established_year": 2023,
            "is_verified": False,
            "is_active": True,
        }
        response = self.client.post(
            self.create_url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Company.objects.count(), 2)

    def test_create_company_with_another_employer(self):
        # self.client.force_authenticate(user=self.user3)
        refresh = RefreshToken.for_user(self.user3)
        self.access_token = str(refresh.access_token)
        # Set authorization header for all requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        data = {
            "name": "New Company",
            "website": "http://newcompany.com",
            "industry": self.industry.id,
            "location": "Los Angeles",
            "description": "A new company",
            "established_year": 2023,
            "is_verified": False,
            "is_active": True,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Company.objects.count(), 2)

    # test to get company from another employer
    def test_get_company_from_another_employer(self):
        refresh = RefreshToken.for_user(self.user3)
        self.access_token = str(refresh.access_token)
        # Set authorization header for all requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("company-internal-detail", args=[self.company2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Finance Inc")
        self.assertEqual(response.data["website"], "http://financeinc.com")
        self.assertEqual(response.data["industry"], self.industry.id)
        self.assertEqual(response.data["location"], "San Francisco")

    # test to get all companies of the logged in user
    def test_get_all_companies_of_user(self):
        url = reverse("company-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if two companies are returned
        self.assertEqual(response.data[0]["name"], "Tech Corp")

    def test_get_all_companies(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if only allowed company is returned
        self.assertEqual(response.data[0]["name"], "Tech Corp")
        

    def test_get_company_detail(self):
        url = reverse("company-public-detail", args=[self.company.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Tech Corp")
        self.assertEqual(response.data["website"], "http://techcorp.com")
        self.assertEqual(response.data["industry"], self.industry.id)
        self.assertEqual(response.data["location"], "New York")
