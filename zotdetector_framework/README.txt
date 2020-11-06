ZOTDETECTOR FRAMEWORK

SYSTEM REQUIREMENTS:
- Java SDK v1.8
- Maven
- Springboot


INSTALLING SPRINGBOOT:
MacOS
1.) "brew tap pivotal/tap"
2.) "brew install springboot"
Homebrew installs spring to /usr/local/bin

Windows
1.) "scoop bucket add extras"
2.) "scoop install springboot"
Scoop installs spring to ~/scoop/apps/springboot/current/bin


MYSQL REQUIREMENTS:
Copy create_table.sql into MySQL database named zotdetectordb at localhost:3306
- username: "root"
- pasword: "password"
Reset SQL root password: https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html


COMPILE AND START APPLICATION:
"mvn spring-boot:run"
Runs on localhost:8080