# bookShop
링크로 책 정보 추가 기능, 추천, 비추천 기능을 갖춘 책 리뷰 페이지

- 제작기간 : 2020.10.29 ~ 30
<br>

## 소개
### 1. 메인

![image](https://user-images.githubusercontent.com/72585287/116179712-c2a9d900-a752-11eb-8949-85807e972aa6.png)
<br>

### 2. 책 추가하기

![책좋2](https://user-images.githubusercontent.com/72585287/116177802-6db89380-a74f-11eb-93d6-0cd0183f7edd.png) 
<br>
<br>

## 📖 API 설계
| 목적 | API주소 (요청방법) | 서버 |클라이언트|
|:----------:|:----------:|:----------:|:---------:|
| 책 불러오기 | `/api/list`<br>(GET)| DB에서 책 리스트를 불러온다 | X |
| 새 링크 저장 | `/api/list`<br>(POST) | 입력된 url에서 책 정보를 긁어 DB에 저장한다 | url을 입력한다 |
| 좋아요 | `/api/like`<br>(POST) | 해당 책의 `like` 수를 +1 하여 업데이트한다 | 좋아요 버튼 눌린 책의 이름을 전달한다 |
| 별로에요 | `/api/like`<br>(POST) | 해당 책의 `like` 수를 -1 하여 업데이트한다 | 별로에요 버튼 눌린 책의 이름을 전달한다 |
