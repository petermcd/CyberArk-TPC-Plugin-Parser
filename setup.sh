function finish {
    # Output a finishing message and delete this script
    printf '\r\n'
    printf '\r\n'
    read -rp 'I am going to delete myself now, press enter to continue'
    rm 'setup.sh'
}

function header {
    # Output a header for the given section
    printf '\r\n'
    echo "-------------------- $1 --------------------"
    printf '\r\n'
}

header 'General Information'

current_year=$(date +'%Y')
read -rp 'What is your GitHub username? ' github_username

function funding_setup {
    # Setup funding information
    header 'Funding Setup'
    read -rp 'Would you like to setup funding for this project? (y/n) ' funding_y_n
    if [ "$funding_y_n" = 'y' ]; then
        github_funding_username=$github_username
        read -rp 'Should funding be setup for your GitHub account? (y/n) ' github_funding_y_n
        if [ "$github_funding_y_n" = 'n' ]; then
            read -rp 'Enter the GitHub username to use for funding: ' github_funding_username
        fi
        sed -i '' -e "s/{ USERNAME }/$github_funding_username/g" '.github/FUNDING.yml'
    else
        printf 'Skipping funding setup and deleting .github/FUNDING.yml.'
        rm '.github/FUNDING.yml'
    fi
}

function setup_issue_templates {
    # Setup issue templates
    header 'Bug Report Templates'
    read -rp 'Should bug reports be assigned to a user? (y/n) ' assign_bugs_y_n
    bug_handler=$github_username
    if [ "$assign_bugs_y_n" = 'y' ]; then
        read -rp 'Should bug reports be assigned to you? (y/n) ' assign_bugs_you_y_n
        if [ "$assign_bugs_you_y_n" = 'n' ]; then
            read -rp 'Who should bugs be assigned too? ' bug_handler
        fi
        printf 'Assigning bugs to %s' "$bug_handler"
        sed -i '' -e "s/{ USERNAME }/$bug_handler/g" '.github/ISSUE_TEMPLATE/bug_report.md'
    else
        printf 'Removing the assignment line from bug report template.'
        sed -i '' -e 's/assignees: { USERNAME }//g' '.github/ISSUE_TEMPLATE/bug_report.md'
    fi

    header 'Issue Report Templates'

    read -rp 'Should feature requests be assigned to a user? (y/n) ' assign_features_y_n
    feature_handler=$github_username
    if [ "$assign_features_y_n" = 'y' ]; then
        read -rp 'Should feature requests be assigned to you? (y/n) ' assign_features_you_y_n
        if [ "$assign_features_you_y_n" = 'n' ]; then
            read -rp 'Who should feature requests be assigned too? ' feature_handler
        fi
        printf 'Assigning feature requests to %s' "$feature_handler"
        sed -i '' -e "s/{ USERNAME }/$feature_handler/g" '.github/ISSUE_TEMPLATE/feature_request.md'
    else
        printf 'Removing the assignment line from bug report template.'
        sed -i '' -e 's/assignees: { USERNAME }//g' '.github/ISSUE_TEMPLATE/feature_request.md'
    fi
}

function set_python_version {
    header 'Python Version'
    read -rp 'What is the minimum targetted python version? ' python_min
    python_version_no_dot="${python_min//.}"
    sed -i '' -e "s/{ PYTHON VERSION }/$python_min/g" '.github/workflows/uv.yml'
    sed -i '' -e "s/{ PYTHON VERSION }/$python_min/g" '.python-version'
    sed -i '' -e "s/{ PYTHON VERSION }/$python_min/g" 'pyproject.toml'
    sed -i '' -e "s/{ PYTHON VERSION NO DOT }/$python_version_no_dot/g" 'pyproject.toml'
    sed -i '' -e "s/{ PYTHON VERSION }/$python_min/g" 'sonar-project.properties'

    printf 'Updating the Python version across the project.'
}

function setup_licence {
    # Setup licence information
    header "LICENSE File."
    read -rp 'What name should the copyright be under? ' copyright_name
    sed -i '' -e "s/{ YEAR }/$current_year/g" 'LICENSE'
    sed -i '' -e "s/{ YOUR NAME OR YOUR COMPANY NAME }/$copyright_name/g" 'LICENSE'
    printf 'Updated LICENSE file with your name and current year.'
}

function setup_sonar {
    # Setup SonarQube information
    header 'SonarQube Setup'
    read -rp 'Would you like to setup SonarQube for this project? (y/n) ' sonar_y_n
    if [ "$sonar_y_n" = 'y' ]; then
        read -rp 'What is the SonarQube server URL? ' sonar_server_url
        read -rp 'What is the SonarQube project key? ' sonar_project_key

        sonar_server_url_safe="${sonar_server_url//\//\/}"
        sonar_server_url_safe="${sonar_server_url_safe//./\.}"

        printf 'Updating .sonarlint/connectedMode.json with the url and key provided.'
        sed -i '' -e "s/{ SONARQUBE URL }/${sonar_server_url_safe}/g" '.sonarlint/connectedMode.json'
        sed -i '' -e "s/{ SONARQUBE PROJECT KEY }/$sonar_project_key/g" '.sonarlint/connectedMode.json'

        printf '\r\n'

        printf 'Updating sonar-project.properties with the key and source directory provided.'
        sed -i '' -e "s/{ SONARQUBE PROJECT KEY }/$sonar_project_key/g" 'sonar-project.properties'
        sed -i '' -e "s/{ PROJECT SOURCE }/src/g" 'sonar-project.properties'
    else
        printf 'Removing Sonar related files.'
        rm 'sonar-project.properties'
        rm -rf '.sonarlint'
    fi
}

setup_licence
set_python_version
funding_setup
setup_issue_templates
setup_sonar

finish
