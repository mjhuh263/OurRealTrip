![our-real-trip](https://user-images.githubusercontent.com/75108432/111068776-848f8780-850d-11eb-8f2c-6f7c5949f210.png)

# OurRealTrip

## 팀 구성원
프론트엔드 3명, 백엔드 3명
<br>

## 프로젝트 기간
2021.03.02 ~ 2021.03.12
<br>

## 기술 스택
Python, Django, MySQL
<br>

## 프로젝트 설명 
마이리얼트립을 모티브로 진행한 크라우드 펀딩 웹사이트 프로젝트입니다.
<br>

### Document

[API Document](https://www.notion.so/API-Document-1cf78af22e05467487da83827bf5ea9f, "API Document")

<br>

## 프로젝트 결과 시연 영상

[Youtube](https://www.youtube.com/watch?v=bpsRyUtgs-8)

## 프로젝트 구조
프로젝트 구조는 아래와 같습니다.
<br>

Project: 
- config

Apps:
- user
- order
- flight
- accommodation
<br>

```
.
├── Dockerfile
├── README.md
├── accommodation
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20210305_1415.py
│   │   ├── 0003_room_option.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── flight
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── order
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20210311_1318.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── pull_request_template.md
├── requirements.txt
├── setting_up.sh
└── user
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_auto_20210304_2130.py
    │   ├── 0003_user_kakao_id.py
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    └── views.py
```

<br>

### ERD
[Aquery Tool](https://aquerytool.com/aquerymain/index/?rurl=87d8b805-63fd-481a-b942-7cad6c424c64) (pw: 47k3aj)

## 구현 기능 

### 모델링

- ERD(관계형 모델링 설계) 및 model 생성 / Aquery Tool을 활용한 항공, 숙박 모델링 구현 및 models.py 생성
- DB CSV 파일 작성
- db_uploader.py 작성

<br>

### 회원가입 및 로그인 (SignUp & SignIn)

- bcrypt를 사용한 암호화
- 자체 로그인 기능 구현 및 unit test 
- jwt access token 전송 및 유효성 검사 기능 구현
- 카카오 소셜 로그인 구현 및 unit test
- 비회원, 회원 decorator 기능 구현 

<br>

### 숙소

- 숙소 리스트 기능 구현 / Django ORM(Q객체, chianing, annotate, aggregate 등)을 활용한 다양한 filtering 구현 및 unit test
- 숙소 상세 페이지 / user의 입력값과 맞는 데이터를 바탕으로 예약 가능한 숙소 room 불러오기 구현 및 unit test
- 숙소 예약 기능 구현 / POST 요청정보 DB에 Create 구현 및 unit test 
- Django ORM-DB Query / select_related, prefetch_related를 통한 Caching 활용

<br>

### 항공

- 항공 리스트 기능 구현 / Django ORM(Q객체, chianing 등)을 활용한 다양한 filtering 구현 및 unit test
- 항공 예약 기능 구현 / POST 요청정보 DB에 Create 구현 및 unit test 
- Django ORM-DB QUERY / select_related를 통한 Caching 활용

<br>

### 배포 

- 데이스베이스 구축 및 배포 / AWS(EC2, RDS) 데이터베이스 구축 및 배포

<br>

## 프로젝트 Set- Up 

1. **Miniconda(가상환경 tool) 설치** <br>
[제 블로그 게시물](https://velog.io/@mjhuh263/TIL-47-Python-Installing-Miniconda3-and-creating-virtual-envs-%EB%AF%B8%EB%8B%88%EC%BD%98%EB%8B%A4-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0)에 적어 놓았습니다.

<br>

2. **Database 생성**
```
$ mysql server start
$ mysql -u root -p 
$ mysql> create database ourealtrip character set utf8mb4 collate utf8mb4_general_ci;
```
<br>

3. **프로젝트에 필요한 python package 설치**
```
$ pip install django
$ pip install django-cors-headers
$ pip install mysqlclient
```
<br>

3. **Django Project, App 생성**
```
$ django-admin startproject config
$ cd project
$ python manage.py startapp user
$ python manage.py startapp order
$ python manage.py startapp flight
$ python manage.py startapp accommodation
```
<br>

4. **.gitignore 생성** <br>
```
cd ourrelatrip -> project folder name
touch .gitignore
vi .gitignore -> ignore하고 싶은 키워드 추가하고 저장
```
5. **보안 파일 생성** <br>
프로젝트 파일 settings.py 속 secret key 및 database 정보를 `my_settings.py`으로 따로 관리한다.

my_settings.py 생성:
```
cd ourrealtrip -> project folder name
touch my_settings.py
vi my_settings.py
```
+) my_settings.py를 꼭 .gitignore에 추가한다.

my_settings.py 속 정보:
```
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ourrealtrip',
        'USER': 'DB 계정명',
        'PASSWORD': 'DB 비밀번호',
        'HOST': 'DB 주소',
        'PORT': '포트번호',
    }
}

SECRET = 'django에서 생성한 시크릿키'
```
<br>