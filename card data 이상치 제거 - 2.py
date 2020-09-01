import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 작업 디렉토리 지정
os.chdir('C:\\Users\\Msi\\Desktop\\공모전\\카드소비 프로젝트\\데이터')

# seaborn을 사용하여 그릴 때 배경을 바꿔준다.
# 배경을 바꾸게 되면 폰트가 초기화되기 때문에 폰트를 설정하기 전에 미리 설정해주도록 한다.
sns.set_style('darkgrid')

# 한글 폰트가 깨지기 때문에 폰트를 바꿔준다.
font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
rc('font', family=font_name)

# 카드 소비데이터 가져오기 - PPT 12장 그림 1
card = pd.read_csv('CARD_SPENDING_190809.txt', sep='\t')
card_kr = pd.read_csv('card_kr.csv')

jongno_name = ['청운효자동', '사직동', '삼청동', '부암동', '평창동', '무악동',
               '교남동', '가회동', '종로1.2.3.4가동', '종로5.6가동', '이화동',
               '혜화동', '창신1동', '창신2동', '창신3동', '숭인1동', '숭인2동']

nowon_name = ['월계1동', '월계2동', '월계3동', '공릉1동', '공릉2동', '하계1동',
              '하계2동', '중계본동', '중계1동', '중계4동', '중계2.3동', '상계1동',
              '상계2동', '상계3.4동', '상계5동', '상계6.7동', '상계8동', '상계9동', '상계10동']


mct_name = ['숙박(10)', '레저용품(20)', '레저업소(21)', '문화취미(22)', '가구(30)', '전기(31)', 
            '주방용구(32)', '연료판매(33)', '광학제품(34)', '가전(35)', '유통업(40)', '의복(42)',
            '직물(43)', '신변잡화(44)', '서적문구(50)', '사무통신(52)', '자동차판매(60)', '자동차정비(62)',
            '의료기관(70)', '보건위생(71)', '요식업소(80)', '음료식품(81)', '수리서비스(92)']

age_name = ['25세 미만', '25세~29세', '30세~34세', '35세~39세', '40세~44세',
            '45세~49세', '50세~54세', '55세~59세', '60세~64세', '65세 이상']

# 이상치 제거에 앞서 어떻게 제거를 해야할지 생각을 해본다.

# 1. 전체 데이터의 이상치를 제거하게 된다면 업종별로 판매하는 물건의 가격이 다르기 때문에
# 고가의 물건을 취급하는 업종들만 제거될 것이다. ex) 가구, 가전, 의료기관
# 해결 방법 : 데이터를 업종별로 나누고 이상치를 제거한다.

# 2. 소비 건수가 많으면 소비 금액도 많아질 수 밖에 없다.
# 해결 방법 : 소비 금액을 소비 건수로 나눈 평균 소비 금액 column을 추가한다.

# 1, 2번 문제를 합하여 업종별 평균 소비 금액으로 이상치를 제거한다.

# 평균 소비 금액 column 추가
card_kr['USE'] = round(card_kr['USE_AMT'] / card_kr['USE_CNT'], 2)

# 전체 데이터에서 업종별 소비 금액에 대한 boxplot 확인
# 실제로 구별, 동별, 나이별, 성별, 업종별로 평균 소비 금액의 분포에 대해 알아본다.

# 구별 평균 소비 금액 분포는 크게 차이가 없었다.
plt.figure(figsize=(8, 4))
sns.boxplot(x='GU_CD', y='USE_AMT', data = card_kr, order = ['종로구', '노원구'])
plt.title('구별 평균 소비 금액', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('행정구', fontsize=15)
plt.ylabel('평균 소비 금액', fontsize=15)
plt.ylim(0, 5000)
plt.show()

# 동별 평균 소비 금액 분포는 차이 조금 있지만 명확한 차이는 없다.
plt.figure(figsize=(8, 4))
sns.boxplot(x='DONG_CD', y='USE_AMT', data = card_kr, order = jongno_name + nowon_name)
plt.title('동별 평균 소비 금액', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('행정동', fontsize=15)
plt.ylabel('평균 소비 금액', fontsize=15)
plt.ylim(0, 10000)
plt.show()

# 업종별 평균 소비 금액 분포에서 많은 차이를 보였다.
plt.figure(figsize=(8, 4))
sns.boxplot(x='MCT_CAT_CD', y='USE_AMT', data = card_kr, order = mct_name)
plt.title('업종별 평균 소비 금액', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('업종', fontsize=15)
plt.ylabel('평균 소비 금액', fontsize=15)
plt.ylim(0, 8000)
plt.show()

# 성별 평균 소비 금액 분포는 크게 차이가 없었다.
plt.figure(figsize=(8, 4))
sns.boxplot(x='SEX_CD', y='USE_AMT', data = card_kr, order = ['남자', '여자'])
plt.title('성별 평균 소비 금액', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('성별', fontsize=15)
plt.ylabel('평균 소비 금액', fontsize=15)
plt.ylim(0, 5000)
plt.show()

# 연령별 평균 소비 금액 분포는 나이가 많을 수록 조금씩 늘었지만 별 차이가 없었다.
plt.figure(figsize=(8, 4))
sns.boxplot(x='AGE_CD', y='USE_AMT', data = card_kr, order = age_name)
plt.title('연령별 평균 소비 금액', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('연령', fontsize=15)
plt.ylabel('평균 소비 금액', fontsize=15)
plt.ylim(0, 5000)
plt.show()

# 평균 소비 금액에 대한 boxplot - PPT 14장 그림 1
plt.figure(figsize=(8, 4))
sns.boxplot(x='MCT_CAT_CD', y='USE', data = card_kr, order = mct_name)
plt.title('업종별 평균 소비 금액', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('업종', fontsize=15)
plt.ylabel('소비 금액', fontsize=15)
plt.show()

# 평균 소비 금액에 대한 boxplot - PPT 14장 그림 2
plt.figure(figsize=(8, 4))
sns.boxplot(x='MCT_CAT_CD', y='USE', data = card_kr, order = mct_name)
plt.title('업종별 평균 소비 금액', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('업종', fontsize=15)
plt.ylabel('평균 소비 금액', fontsize=15)
plt.ylim(0, 500)
plt.show()

# 위에서 업종별 평균 소비 금액이 서로 상이한 값을 가지므로 이상치 제거는
# 업종별 평균 소비 금액을 기준으로 하도록 한다.

# 이상치 제거 - PPT 15장 그림 1
card_outlier = pd.DataFrame()
def card_outlier_remove(mct_name):
    card_outlier = card_kr[card_kr['MCT_CAT_CD'] == mct_name]
    Q1 = card_outlier['USE'].quantile(q=0.25)
    Q3 = card_outlier['USE'].quantile(q=0.75)
    IQR = Q3 - Q1
    step = 1.5 * IQR
    outlier_remove = card_outlier[(card_outlier['USE'] > Q1 - step) & 
                                  (card_outlier['USE'] < Q3 + step)]
    return outlier_remove

card_outlier = pd.concat([card_outlier_remove(i) for i in mct_name])

# 이상치 제거 후 길이 비교 - PPT 15장 그림 2
plt.figure(figsize=(3, 4))
g = sns.barplot(['제거 전', '제거 후'], [len(card_kr), len(card_outlier)])
g.annotate(len(card_kr), (g.patches[0].get_x() + g.patches[0].get_width() / 2., g.patches[0].get_height()), ha = 'center', va = 'center', xytext = (0, 4), textcoords = 'offset points')
g.annotate(len(card_outlier), (g.patches[1].get_x() + g.patches[1].get_width() / 2., g.patches[1].get_height()), ha = 'center', va = 'center', xytext = (0, 4), textcoords = 'offset points')
plt.show()

# 이상치 제거 후
plt.figure(figsize=(8, 4))
sns.boxplot(x='MCT_CAT_CD', y='USE', data = card_outlier, order = mct_name)
plt.title('업종별 1회 카드 사용 시 소비 금액에 대한 boxplot', fontsize=17, position=(0.5, 1.05))
plt.xticks(rotation=60, fontsize=11)
plt.xlabel('업종', fontsize=15)
plt.ylabel('소비 금액', fontsize=15)
plt.ylim(0, 300)
plt.show()

# 이상치 제거 후 csv 파일 저장
card_outlier.to_csv('card_outlier.csv', index=False)
