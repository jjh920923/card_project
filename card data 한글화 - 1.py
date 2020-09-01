import os
import pandas as pd
from matplotlib import font_manager, rc

# 작업 디렉토리 지정
os.chdir('C:\\Users\\Msi\\Desktop\\공모전\\카드소비 프로젝트\\데이터')

# 한글 폰트가 깨지기 때문에 폰트를 바꿔준다.
font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
rc('font', family=font_name)

# 카드 소비데이터 가져오기 - PPT 12장 그림 1
card = pd.read_csv('CARD_SPENDING_190809.txt', sep='\t')

# 결측치 확인
card.isnull().sum()

# 코드로 되어있는 데이터를 한글버전으로 복사하기
card_kr = card.copy()

# 한글 변환 - PPT 12장 그림 2
# 구 코드를 한글로 변환
card_kr['GU_CD'][card_kr['GU_CD'] == 110] = '종로구'
card_kr['GU_CD'][card_kr['GU_CD'] == 350] = '노원구'

# 동 코드 중에 중복되는 코드가 존재하기 때문에 구를 나누고 데이터를 변형한다.
card_jongno = card_kr[card_kr['GU_CD'] == '종로구']
card_nowon = card_kr[card_kr['GU_CD'] == '노원구']

# 동 코드를 한글로 변환
jongno_code = [515, 530, 540, 550, 560, 570, 580, 600, 615, 630, 640, 650, 670, 680, 690, 700, 710]
jongno_name = ['청운효자동', '사직동', '삼청동', '부암동', '평창동', '무악동',
               '교남동', '가회동', '종로1.2.3.4가동', '종로5.6가동', '이화동',
               '혜화동', '창신1동', '창신2동', '창신3동', '숭인1동', '숭인2동']

nowon_code = [560, 570, 580, 595, 600, 611, 612, 619, 621, 624, 625, 630, 640, 665, 670, 695, 700, 710, 720]
nowon_name = ['월계1동', '월계2동', '월계3동', '공릉1동', '공릉2동', '하계1동',
              '하계2동', '중계본동', '중계1동', '중계4동', '중계2.3동', '상계1동',
              '상계2동', '상계3.4동', '상계5동', '상계6.7동', '상계8동', '상계9동', '상계10동']

card_jongno['DONG_CD'] = card_jongno['DONG_CD'].replace(jongno_code, jongno_name)
card_nowon['DONG_CD'] = card_nowon['DONG_CD'].replace(nowon_code, nowon_name)

# 분리한 구별 데이터를 변형 후 다시 결합
card_kr = pd.concat([card_jongno, card_nowon])

# 상품 카테고리 코드를 한글로 변환
mct_code = [10, 20, 21, 22, 30, 31, 32, 33, 34, 35, 40, 42, 43, 44, 50, 52, 60, 62, 70, 71, 80, 81, 92]
mct_name = ['숙박(10)', '레저용품(20)', '레저업소(21)', '문화취미(22)', '가구(30)', '전기(31)', 
            '주방용구(32)', '연료판매(33)', '광학제품(34)', '가전(35)', '유통업(40)', '의복(42)',
            '직물(43)', '신변잡화(44)', '서적문구(50)', '사무통신(52)', '자동차판매(60)', '자동차정비(62)',
            '의료기관(70)', '보건위생(71)', '요식업소(80)', '음료식품(81)', '수리서비스(92)']

card_kr['MCT_CAT_CD'] = card_kr['MCT_CAT_CD'].replace(mct_code, mct_name)

# 성별 코드를 한글로 변환
card_kr["SEX_CD"] = card_kr["SEX_CD"].replace(['M', 'F'], ['남자', '여자'])

# 나이 코드를 한글로 변환
age_code = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
age_name = ['25세 미만', '25세~29세', '30세~34세', '35세~39세', '40세~44세',
            '45세~49세', '50세~54세', '55세~59세', '60세~64세', '65세 이상']

card_kr['AGE_CD'] = card_kr['AGE_CD'].replace(age_code, age_name)

# 다음번에 프로젝트를 이어할 때 시간단축을 위해 csv 파일로 따로 저장해 놓는다.
card_kr.to_csv('card_kr.csv', index=False)