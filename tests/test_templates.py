"""
Unit tests for template modules
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.templates.login import LoginTestTemplate, LoginPageObjectTemplate
from src.templates.selenium_keywords import AdvancedSeleniumKeywords
from src.templates.extended_keywords import ExtendedSeleniumKeywords
from src.templates.performance import PerformanceTestTemplate
from src.templates.api import APITestTemplate
from src.templates.data_driven import DataDrivenTestTemplate
from src.templates.mobile import MobileTestTemplate
from src.templates.visual import VisualRegressionTemplate
from src.templates.database import DatabaseTestTemplate
from src.templates.cicd import CICDTemplate


class TestLoginTestTemplate:
    """Tests for LoginTestTemplate"""
    
    def test_generate_basic_login_test(self):
        """Test generating basic login test"""
        template = LoginTestTemplate()
        result = template.generate(
            url="https://example.com",
            username="testuser",
            password="testpass"
        )
        
        assert "*** Settings ***" in result
        assert "*** Variables ***" in result
        assert "*** Test Cases ***" in result
        assert "https://example.com" in result
        assert "testuser" in result
    
    def test_generate_with_negative_tests(self):
        """Test generating login test with negative tests"""
        template = LoginTestTemplate()
        result = template.generate(
            url="https://example.com",
            username="testuser",
            password="testpass",
            include_negative_tests=True
        )
        
        assert "Invalid Username Test" in result
        assert "Invalid Password Test" in result
        assert "Empty Credentials Test" in result
    
    def test_generate_with_headless(self):
        """Test generating login test with headless mode"""
        template = LoginTestTemplate()
        result = template.generate(
            url="https://example.com",
            username="testuser",
            password="testpass",
            headless=True
        )
        
        assert "headless" in result.lower()
    
    def test_generate_with_different_templates(self):
        """Test generating with different selector templates"""
        template = LoginTestTemplate()
        
        for template_type in ["generic", "bootstrap", "materialui"]:
            result = template.generate(
                url="https://example.com",
                username="testuser",
                password="testpass",
                template_type=template_type
            )
            assert "*** Test Cases ***" in result


class TestLoginPageObjectTemplate:
    """Tests for LoginPageObjectTemplate"""
    
    def test_generate_page_object(self):
        """Test generating page object"""
        template = LoginPageObjectTemplate()
        result = template.generate()
        
        assert "*** Settings ***" in result
        assert "*** Variables ***" in result
        assert "*** Keywords ***" in result
        assert "Input Username" in result
        assert "Input Password" in result
    
    def test_generate_with_wait_keywords(self):
        """Test generating with wait keywords"""
        template = LoginPageObjectTemplate()
        result = template.generate(include_wait_keywords=True)
        
        assert "Wait For Login Page" in result
    
    def test_generate_with_validation_keywords(self):
        """Test generating with validation keywords"""
        template = LoginPageObjectTemplate()
        result = template.generate(include_validation_keywords=True)
        
        assert "Verify Login Success" in result
        assert "Verify Login Failure" in result


class TestAdvancedSeleniumKeywords:
    """Tests for AdvancedSeleniumKeywords"""
    
    def test_generate_keywords(self):
        """Test generating advanced keywords"""
        template = AdvancedSeleniumKeywords()
        result = template.generate()
        
        assert "*** Settings ***" in result
        assert "*** Keywords ***" in result
        assert "Select Dropdown Option By Label" in result
        assert "Select Checkbox If Not Selected" in result
        assert "Handle Alert And Accept" in result
        assert "Hover Over Element" in result
        assert "Scroll To Element" in result


class TestExtendedSeleniumKeywords:
    """Tests for ExtendedSeleniumKeywords"""
    
    def test_generate_keywords(self):
        """Test generating extended keywords"""
        template = ExtendedSeleniumKeywords()
        result = template.generate()
        
        assert "*** Settings ***" in result
        assert "Capture Full Page Screenshot" in result
        assert "Get Page Performance Metrics" in result
        assert "Set Viewport Size" in result


class TestPerformanceTestTemplate:
    """Tests for PerformanceTestTemplate"""
    
    def test_generate_performance_test(self):
        """Test generating performance test"""
        template = PerformanceTestTemplate()
        result = template.generate()
        
        assert "*** Settings ***" in result
        assert "*** Test Cases ***" in result
        assert "Page Load Performance Test" in result
        assert "Collect Performance Metrics" in result
    
    def test_generate_with_custom_thresholds(self):
        """Test generating with custom thresholds"""
        template = PerformanceTestTemplate()
        result = template.generate(
            load_threshold_ms=5000,
            dom_ready_threshold_ms=3000
        )
        
        assert "5000" in result
        assert "3000" in result


class TestAPITestTemplate:
    """Tests for APITestTemplate"""
    
    def test_generate_api_test(self):
        """Test generating API test"""
        template = APITestTemplate()
        result = template.generate(
            base_url="https://api.example.com",
            endpoint="/users"
        )
        
        assert "*** Settings ***" in result
        assert "RequestsLibrary" in result
        assert "https://api.example.com" in result
        assert "/users" in result
    
    def test_generate_with_crud(self):
        """Test generating with CRUD tests"""
        template = APITestTemplate()
        result = template.generate(
            base_url="https://api.example.com",
            include_crud=True
        )
        
        assert "Create Resource" in result
        assert "Read Resource" in result
        assert "Update Resource" in result
        assert "Delete Resource" in result
    
    def test_generate_with_auth(self):
        """Test generating with auth tests"""
        template = APITestTemplate()
        result = template.generate(
            base_url="https://api.example.com",
            include_auth=True
        )
        
        assert "Authentication" in result
        assert "Token" in result


class TestDataDrivenTestTemplate:
    """Tests for DataDrivenTestTemplate"""
    
    def test_generate_login_data_driven(self):
        """Test generating login data-driven test"""
        template = DataDrivenTestTemplate()
        result = template.generate(test_type="login")
        
        assert "*** Settings ***" in result
        assert "DataDriver" in result
        assert "Login Test" in result
    
    def test_generate_form_data_driven(self):
        """Test generating form data-driven test"""
        template = DataDrivenTestTemplate()
        result = template.generate(test_type="form")
        
        assert "Form Submission Test" in result
    
    def test_generate_with_setup_instructions(self):
        """Test generating with setup instructions"""
        template = DataDrivenTestTemplate()
        result = template.generate(include_setup=True)
        
        assert "TEST DATA FILE SETUP" in result


class TestMobileTestTemplate:
    """Tests for MobileTestTemplate"""
    
    def test_generate_android_test(self):
        """Test generating Android test"""
        template = MobileTestTemplate()
        result = template.generate(platform="android")
        
        assert "*** Settings ***" in result
        assert "AppiumLibrary" in result
        assert "Android" in result
    
    def test_generate_ios_test(self):
        """Test generating iOS test"""
        template = MobileTestTemplate()
        result = template.generate(platform="ios")
        
        assert "iOS" in result
        assert "XCUITest" in result
    
    def test_generate_with_gestures(self):
        """Test generating with gesture keywords"""
        template = MobileTestTemplate()
        result = template.generate(include_gestures=True)
        
        assert "Swipe Left" in result
        assert "Swipe Right" in result
        assert "Pinch" in result


class TestVisualRegressionTemplate:
    """Tests for VisualRegressionTemplate"""
    
    def test_generate_visual_test(self):
        """Test generating visual regression test"""
        template = VisualRegressionTemplate()
        result = template.generate()
        
        assert "*** Settings ***" in result
        assert "Visual" in result
        assert "Baseline" in result
        assert "Compare" in result


class TestDatabaseTestTemplate:
    """Tests for DatabaseTestTemplate"""
    
    def test_generate_postgresql_test(self):
        """Test generating PostgreSQL test"""
        template = DatabaseTestTemplate()
        result = template.generate(db_type="postgresql")
        
        assert "*** Settings ***" in result
        assert "DatabaseLibrary" in result
        assert "psycopg2" in result
    
    def test_generate_mysql_test(self):
        """Test generating MySQL test"""
        template = DatabaseTestTemplate()
        result = template.generate(db_type="mysql")
        
        assert "pymysql" in result
    
    def test_generate_with_crud(self):
        """Test generating with CRUD tests"""
        template = DatabaseTestTemplate()
        result = template.generate(include_crud=True)
        
        assert "Insert Record Test" in result
        assert "Select Record Test" in result
        assert "Update Record Test" in result
        assert "Delete Record Test" in result


class TestCICDTemplate:
    """Tests for CICDTemplate"""
    
    def test_generate_github_actions(self):
        """Test generating GitHub Actions config"""
        template = CICDTemplate()
        result = template.generate(platform="github")
        
        assert "GitHub Actions" in result
        assert "runs-on" in result
        assert "steps:" in result
    
    def test_generate_gitlab_ci(self):
        """Test generating GitLab CI config"""
        template = CICDTemplate()
        result = template.generate(platform="gitlab")
        
        assert "GitLab CI" in result
        assert "stages:" in result
    
    def test_generate_jenkinsfile(self):
        """Test generating Jenkinsfile"""
        template = CICDTemplate()
        result = template.generate(platform="jenkins")
        
        assert "Jenkinsfile" in result
        assert "pipeline" in result
    
    def test_generate_azure_pipelines(self):
        """Test generating Azure Pipelines config"""
        template = CICDTemplate()
        result = template.generate(platform="azure")
        
        assert "Azure Pipelines" in result
        assert "trigger:" in result
    
    def test_generate_with_parallel(self):
        """Test generating with parallel execution"""
        template = CICDTemplate()
        result = template.generate(platform="github", include_parallel=True)
        
        assert "parallel" in result.lower() or "pabot" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
