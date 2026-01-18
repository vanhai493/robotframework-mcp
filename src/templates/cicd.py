"""
CI/CD integration templates for Robot Framework
"""

from .base import BaseTemplate


class CICDTemplate(BaseTemplate):
    """Template for generating CI/CD configuration files"""
    
    def generate(
        self,
        platform: str = "github",
        test_command: str = "robot",
        python_version: str = "3.11",
        include_parallel: bool = True,
    ) -> str:
        """
        Generate CI/CD configuration
        
        Args:
            platform: CI/CD platform (github, gitlab, jenkins, azure)
            test_command: Command to run tests
            python_version: Python version to use
            include_parallel: Include parallel execution config
        """
        if platform.lower() == "github":
            return self._generate_github_actions(test_command, python_version, include_parallel)
        elif platform.lower() == "gitlab":
            return self._generate_gitlab_ci(test_command, python_version, include_parallel)
        elif platform.lower() == "jenkins":
            return self._generate_jenkinsfile(test_command, python_version, include_parallel)
        elif platform.lower() == "azure":
            return self._generate_azure_pipelines(test_command, python_version, include_parallel)
        else:
            return self._generate_github_actions(test_command, python_version, include_parallel)
    
    def _generate_github_actions(
        self, test_command: str, python_version: str, include_parallel: bool
    ) -> str:
        parallel_config = ""
        if include_parallel:
            parallel_config = """
      - name: Run Tests in Parallel
        run: |
          pip install pabot
          pabot --processes 4 --outputdir results tests/
"""
        
        return f"""# GitHub Actions workflow for Robot Framework tests
# Save as: .github/workflows/robot-tests.yml

name: Robot Framework Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:

env:
  PYTHON_VERSION: '{python_version}'

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        browser: [chrome, firefox]
      fail-fast: false
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{{{ env.PYTHON_VERSION }}}}
          cache: 'pip'

      - name: Install Chrome
        if: matrix.browser == 'chrome'
        uses: browser-actions/setup-chrome@latest

      - name: Install Firefox
        if: matrix.browser == 'firefox'
        uses: browser-actions/setup-firefox@latest

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install robotframework robotframework-seleniumlibrary webdrivermanager
          webdrivermanager chrome firefox --linkpath /usr/local/bin

      - name: Run Robot Framework tests
        run: |
          {test_command} --variable BROWSER:${{{{ matrix.browser }}}} \\
            --outputdir results \\
            --loglevel DEBUG \\
            tests/
        continue-on-error: true
{parallel_config}
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: robot-results-${{{{ matrix.browser }}}}
          path: results/
          retention-days: 30

      - name: Publish Test Report
        uses: joonvena/robotframework-reporter-action@v2.4
        if: always()
        with:
          gh_access_token: ${{{{ secrets.GITHUB_TOKEN }}}}
          report_path: results

  notify:
    needs: test
    runs-on: ubuntu-latest
    if: failure()
    steps:
      - name: Notify on failure
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          fields: repo,message,commit,author
        env:
          SLACK_WEBHOOK_URL: ${{{{ secrets.SLACK_WEBHOOK }}}}
"""
    
    def _generate_gitlab_ci(
        self, test_command: str, python_version: str, include_parallel: bool
    ) -> str:
        parallel_config = ""
        if include_parallel:
            parallel_config = """
test:parallel:
  stage: test
  script:
    - pip install pabot
    - pabot --processes 4 --outputdir results tests/
  artifacts:
    paths:
      - results/
    when: always
  parallel: 4
"""
        
        return f"""# GitLab CI configuration for Robot Framework tests
# Save as: .gitlab-ci.yml

image: python:{python_version}

stages:
  - setup
  - test
  - report

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"
  BROWSER: "chrome"

cache:
  paths:
    - .pip-cache/
    - .venv/

before_script:
  - apt-get update -qq
  - apt-get install -y -qq chromium chromium-driver firefox-esr
  - python -m venv .venv
  - source .venv/bin/activate
  - pip install --upgrade pip
  - pip install robotframework robotframework-seleniumlibrary

setup:
  stage: setup
  script:
    - pip install -r requirements.txt
  artifacts:
    paths:
      - .venv/

test:chrome:
  stage: test
  script:
    - source .venv/bin/activate
    - {test_command} --variable BROWSER:chrome --outputdir results tests/
  artifacts:
    paths:
      - results/
    reports:
      junit: results/output.xml
    when: always
  allow_failure: false

test:firefox:
  stage: test
  script:
    - source .venv/bin/activate
    - {test_command} --variable BROWSER:firefox --outputdir results tests/
  artifacts:
    paths:
      - results/
    when: always
  allow_failure: true
{parallel_config}
report:
  stage: report
  script:
    - source .venv/bin/activate
    - pip install robotframework-metrics
    - robotmetrics --inputpath results/ --output results/metrics.html
  artifacts:
    paths:
      - results/
    when: always
  dependencies:
    - test:chrome
    - test:firefox

pages:
  stage: report
  script:
    - mkdir -p public
    - cp -r results/* public/
  artifacts:
    paths:
      - public
  only:
    - main
"""
    
    def _generate_jenkinsfile(
        self, test_command: str, python_version: str, include_parallel: bool
    ) -> str:
        parallel_config = ""
        if include_parallel:
            parallel_config = """
        stage('Parallel Tests') {
            parallel {
                stage('Chrome Tests') {
                    steps {
                        sh 'robot --variable BROWSER:chrome --outputdir results/chrome tests/'
                    }
                }
                stage('Firefox Tests') {
                    steps {
                        sh 'robot --variable BROWSER:firefox --outputdir results/firefox tests/'
                    }
                }
            }
        }
"""
        
        return f"""// Jenkinsfile for Robot Framework tests
// Save as: Jenkinsfile

pipeline {{
    agent any
    
    environment {{
        PYTHON_VERSION = '{python_version}'
        BROWSER = 'chrome'
    }}
    
    options {{
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }}
    
    stages {{
        stage('Setup') {{
            steps {{
                sh '''
                    python{python_version} -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install robotframework robotframework-seleniumlibrary
                '''
            }}
        }}
        
        stage('Run Tests') {{
            steps {{
                sh '''
                    . .venv/bin/activate
                    {test_command} --variable BROWSER:${{BROWSER}} \\
                        --outputdir results \\
                        --loglevel DEBUG \\
                        tests/
                '''
            }}
        }}
{parallel_config}
        stage('Publish Results') {{
            steps {{
                robot outputPath: 'results',
                      passThreshold: 95.0,
                      unstableThreshold: 90.0,
                      otherFiles: '**/*.png'
            }}
        }}
    }}
    
    post {{
        always {{
            archiveArtifacts artifacts: 'results/**/*', fingerprint: true
            
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'results',
                reportFiles: 'report.html',
                reportName: 'Robot Framework Report'
            ])
        }}
        
        failure {{
            emailext (
                subject: "FAILED: Job '${{env.JOB_NAME}} [${{env.BUILD_NUMBER}}]'",
                body: '''${{SCRIPT, template="groovy-html.template"}}''',
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }}
        
        cleanup {{
            cleanWs()
        }}
    }}
}}
"""
    
    def _generate_azure_pipelines(
        self, test_command: str, python_version: str, include_parallel: bool
    ) -> str:
        parallel_config = ""
        if include_parallel:
            parallel_config = """
- stage: ParallelTests
  displayName: 'Parallel Test Execution'
  jobs:
  - job: ParallelRun
    strategy:
      parallel: 4
    steps:
    - script: |
        pip install pabot
        pabot --processes 4 --outputdir $(Build.ArtifactStagingDirectory)/results tests/
      displayName: 'Run Parallel Tests'
"""
        
        return f"""# Azure Pipelines configuration for Robot Framework tests
# Save as: azure-pipelines.yml

trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - README.md
      - docs/*

pr:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '{python_version}'
  browser: 'chrome'

stages:
- stage: Test
  displayName: 'Run Robot Framework Tests'
  jobs:
  - job: TestChrome
    displayName: 'Chrome Tests'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
        addToPath: true
      displayName: 'Use Python $(pythonVersion)'

    - script: |
        sudo apt-get update
        sudo apt-get install -y chromium-browser chromium-chromedriver
      displayName: 'Install Chrome'

    - script: |
        python -m pip install --upgrade pip
        pip install robotframework robotframework-seleniumlibrary webdrivermanager
      displayName: 'Install dependencies'

    - script: |
        {test_command} --variable BROWSER:chrome \\
          --outputdir $(Build.ArtifactStagingDirectory)/results \\
          --loglevel DEBUG \\
          tests/
      displayName: 'Run Robot Framework tests'
      continueOnError: true

    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/output.xml'
        searchFolder: '$(Build.ArtifactStagingDirectory)/results'
        mergeTestResults: true
        testRunTitle: 'Robot Framework Tests - Chrome'
      condition: always()
      displayName: 'Publish test results'

    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: '$(Build.ArtifactStagingDirectory)/results'
        artifactName: 'robot-results-chrome'
      condition: always()
      displayName: 'Publish artifacts'

  - job: TestFirefox
    displayName: 'Firefox Tests'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
        addToPath: true

    - script: |
        sudo apt-get update
        sudo apt-get install -y firefox
      displayName: 'Install Firefox'

    - script: |
        python -m pip install --upgrade pip
        pip install robotframework robotframework-seleniumlibrary webdrivermanager
      displayName: 'Install dependencies'

    - script: |
        {test_command} --variable BROWSER:firefox \\
          --outputdir $(Build.ArtifactStagingDirectory)/results \\
          tests/
      displayName: 'Run Robot Framework tests'
      continueOnError: true

    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: '$(Build.ArtifactStagingDirectory)/results'
        artifactName: 'robot-results-firefox'
      condition: always()
{parallel_config}
- stage: Report
  displayName: 'Generate Reports'
  dependsOn: Test
  condition: always()
  jobs:
  - job: GenerateReport
    steps:
    - task: DownloadBuildArtifacts@0
      inputs:
        buildType: 'current'
        downloadType: 'all'
        downloadPath: '$(Build.ArtifactStagingDirectory)'

    - script: |
        pip install robotframework-metrics
        robotmetrics --inputpath $(Build.ArtifactStagingDirectory) --output metrics.html
      displayName: 'Generate metrics report'
"""
