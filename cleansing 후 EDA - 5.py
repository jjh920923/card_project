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

card_outlier = pd.read_csv('card_outlier.csv')
pop_outlier = pd.read_csv('pop_outlier.csv')

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

# 카드 데이터와 유동인구 데이터 결합 - PPT 19장 그림 1
card = card_outlier.groupby(['STD_DD', 'DONG_CD', 'SEX_CD', 'AGE_CD']).sum()
card = card.reset_index(drop=False)
df = pd.merge(card, pop_outlier)
df['USE'] = round(card['USE_AMT'] / card['USE_CNT'], 2)

# 업종별 카드 소비 건수, 소비 금액 - PPT 21장 그림 1
card_mct = card_outlier.groupby('MCT_CAT_CD').mean()
card_mct = card_mct.drop(['STD_DD'], axis = 1)
card_mct = card_mct.reindex(mct_name)

# 업종별 카드 소비 금액 top3 percentage
card_mct_amt80per = float(card_mct['USE_AMT'][card_mct.index == '요식업소(80)']/card_mct['USE_AMT'].sum() * 100)
card_mct_amt40per = float(card_mct['USE_AMT'][card_mct.index == '유통업(40)']/card_mct['USE_AMT'].sum() * 100)
card_mct_amt70per = float(card_mct['USE_AMT'][card_mct.index == '의료기관(70)']/card_mct['USE_AMT'].sum() * 100)

# 업종별 카드 소비 금액 그래프 - PPT 21장 그림 1
plt.figure(figsize=(9, 7))
g = sns.barplot(card_mct.index, card_mct['USE_AMT'])
g.annotate(str(format(card_mct_amt40per, '.1f'))+'%', (g.patches[10].get_x() + g.patches[10].get_width() / 2., g.patches[10].get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
g.annotate(str(format(card_mct_amt70per, '.1f'))+'%', (g.patches[18].get_x() + g.patches[18].get_width() / 2., g.patches[18].get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
g.annotate(str(format(card_mct_amt80per, '.1f'))+'%', (g.patches[20].get_x() + g.patches[20].get_width() / 2., g.patches[20].get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.title('노원구/종로구 업종별 전체 소비 금액', position=(0.5, 1.05), fontsize = 20)
plt.xlabel('업종', fontsize = 15)
plt.ylabel('소비 금액', fontsize = 15)
plt.xticks(rotation=60)
plt.show()

# 업종별 카드 소비 건수 top3 percentage
card_mct_cnt80per = float(card_mct['USE_CNT'][card_mct.index == '요식업소(80)']/card_mct['USE_CNT'].sum() * 100)
card_mct_cnt40per = float(card_mct['USE_CNT'][card_mct.index == '유통업(40)']/card_mct['USE_CNT'].sum() * 100)
card_mct_cnt50per = float(card_mct['USE_CNT'][card_mct.index == '서적문구(50)']/card_mct['USE_CNT'].sum() * 100)

# 업종별 카드 소비 건수 그래프 - PPT 21장 그림 2
plt.figure(figsize=(9, 7))
g = sns.barplot(card_mct.index, card_mct['USE_CNT'])
g.annotate(str(format(card_mct_cnt40per, '.1f'))+'%', (g.patches[10].get_x() + g.patches[10].get_width() / 2., g.patches[10].get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
g.annotate(str(format(card_mct_cnt50per, '.1f'))+'%', (g.patches[14].get_x() + g.patches[14].get_width() / 2., g.patches[14].get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
g.annotate(str(format(card_mct_cnt80per, '.1f'))+'%', (g.patches[20].get_x() + g.patches[20].get_width() / 2., g.patches[20].get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
plt.title('노원구/종로구 업종별 전체 소비 건수', position=(0.5, 1.05), fontsize = 20)
plt.xlabel('업종', fontsize = 15)
plt.ylabel('소비 건수', fontsize = 15)
plt.xticks(rotation=60)
plt.show()

# 연령대별 소비 건수, 소비 금액
card_age = df.groupby('AGE_CD').mean()
card_age = card_age.drop(['STD_DD'], axis = 1)
card_age['USE'] = round(card_age['USE_AMT'] / card_age['USE_CNT'], 2)


# 연령대별  카드 소비건수 그래프
plt.figure(figsize=(9, 7))
sns.barplot(card_age.index, card_age['USE_CNT'])
plt.title('연령대별 전체 소비 건수', position=(0.5, 1.05), fontsize = 20)
plt.xlabel('나이', fontsize = 15)
plt.ylabel('소비 건수', fontsize = 15)
plt.show()

# 연령대별 카드 소비금액 그래프
plt.figure(figsize=(9, 7))
sns.barplot(card_age.index, card_age['USE_AMT'])
plt.title('연령대별 전체 소비 금액', position=(0.5, 1.05), fontsize = 20)
plt.xlabel('나이', fontsize = 15)
plt.ylabel('소비 금액', fontsize = 15)
plt.show()

# 한번 카드를 사용할 때 지출하는 금액
plt.figure(figsize=(9, 7))
sns.barplot(card_age.index, card_age['USE'])
plt.plot(card_age['USE'], 'ro-')
plt.title('연령대별 평균 소비 금액', position=(0.5, 1.05), fontsize = 20)
plt.xlabel('나이', fontsize = 15)
plt.ylabel('평균 소비 금액', fontsize = 15)
plt.show()

# 연령대별  유동인구 그래프
plt.figure(figsize=(9, 7))
sns.barplot(card_age.index, card_age['POP'])
plt.title('연령대별 유동인구', position=(0.5, 1.05), fontsize = 20)
plt.xlabel('나이', fontsize = 15)
plt.ylabel('유동인구 수', fontsize = 15)
plt.show()


# 요일별 카드 소비건수, 소비금액
def day_of_the_week(x):
    year = int(str(x)[:4])
    month = int(str(x)[4:6])
    day = int(str(x)[6:])
    week = ['월', '화', '수', '목', '금', '토', '일'][pd.datetime(year, month, day).weekday()]
    return week

df['week'] = df['STD_DD'].apply(day_of_the_week)


card_date = df[df['STD_DD'] != 20190331]
card_date = card_date.groupby('week').mean()

card_date = card_date.drop(['STD_DD'], axis = 1)

card_date = pd.concat([card_date[card_date.index == '월'], card_date[card_date.index == '화'], card_date[card_date.index == '수'], card_date[card_date.index == '목'],
                       card_date[card_date.index == '금'], card_date[card_date.index == '토'], card_date[card_date.index == '일']])

# 요일별 소비건수와 소비금액 그래프
plt.figure(figsize=(10, 7))
ax1 = plt.subplot(3, 1, 1)
plt.plot(card_date.index, card_date['USE_CNT'], 'b')
plt.title('요일별 소비건수, 소비금액, 유동인구',  position=(0.5, 1.05), fontsize = 20)
plt.ylabel('소비건수', fontsize = 15)

ax2 = plt.subplot(3, 1, 2)
plt.plot(card_date.index, card_date['USE_AMT'], 'r')
plt.ylabel('소비금액', fontsize = 15)

ax3 = plt.subplot(3, 1, 3)
plt.plot(card_date.index, card_date['POP'], 'g')
plt.xlabel('요일', fontsize = 15)
plt.ylabel('유동인구', fontsize = 15)
plt.show()

def day_of_the_week(x):
    year = int(str(x)[:4])
    month = int(str(x)[4:6])
    day = int(str(x)[6:])
    week = ['월', '화', '수', '목', '금', '토', '일'][pd.datetime(year, month, day).weekday()]
    return week

df['week'] = df['STD_DD'].apply(day_of_the_week)

# 월별 소비건수, 소비금액
def month(x):
    month = str(int(str(x)[4:6])) + '월'
    return month

df['month'] = df['STD_DD'].apply(month)


card_month = df.groupby('month').mean()
card_month = card_month.drop(['STD_DD'], axis = 1)
card_month = pd.concat([card_month.iloc[3:,:], card_month.iloc[:3,:]])

# 월별 소비건수, 소비금액, 유동인구 그래프
plt.figure(figsize=(10, 7))
ax1 = plt.subplot(3, 1, 1)
plt.plot(card_month.index, card_month['USE_CNT'], 'b')
plt.title('월별 소비건수, 소비금액, 유동인구',  position=(0.5, 1.05), fontsize = 20)
plt.ylabel('소비 건수', fontsize = 15)

ax2 = plt.subplot(3, 1, 2)
plt.plot(card_month.index, card_month['USE_AMT'], 'r')
plt.ylabel('소비 금액', fontsize = 15)

ax3 = plt.subplot(3, 1, 3)
plt.plot(card_month.index, card_month['POP'], 'g')
plt.xlabel('월', fontsize = 15)
plt.ylabel('유동인구', fontsize = 15)
plt.show()


# 성별 소비건수, 소비금액
card_sex = df.groupby('SEX_CD').mean()
card_sex = card_sex.drop(['STD_DD'], axis = 1)

# 성별 소비건수, 소비금액 그래프
sns.barplot(card_sex.index, card_sex['USE_CNT'])
plt.title('성별 소비 건수', fontsize = 20, position=(0.5, 1.05))
plt.xlabel('성별', fontsize = 15)
plt.ylabel('소비건수', fontsize = 15)
plt.show()

sns.barplot(card_sex.index, card_sex['USE_AMT'])
plt.title('성별 소비 금액', fontsize = 20, position=(0.5, 1.05))
plt.xlabel('성별', fontsize = 15)
plt.ylabel('소비금액', fontsize = 15)
plt.show()

sns.barplot(card_sex.index, card_sex['POP'])
plt.title('성별 유동인구', fontsize = 20, position=(0.5, 1.05))
plt.xlabel('성별', fontsize = 15)
plt.ylabel('유동인구', fontsize = 15)
plt.show()

# 행정동별 소비건수, 소비금액
card_dong = pd.DataFrame(df.groupby(['DONG_CD']).mean())
card_dong = card_dong.drop(['STD_DD'], axis = 1)
card_dong = card_dong.reindex(jongno_name + nowon_name)

# 행정동별 소비건수, 소비금액 그래프
plt.figure(figsize=(10, 7))
sns.barplot(card_dong.index, card_dong['USE_AMT'])
plt.axvline(x=16.5, color='r', linestyle='--')
plt.xticks(rotation=75, fontsize = 12)
plt.title('행정동별 소비 금액', fontsize = 20, position=(0.5, 1.05))
plt.xlabel('종로구                                               노원구', fontsize = 15)
plt.ylabel('소비금액', fontsize = 15)
plt.show()

plt.figure(figsize=(10, 7))
sns.barplot(card_dong.index, card_dong['USE_CNT'])
plt.axvline(x=16.5, color='r', linestyle='--')
plt.xticks(rotation=75, fontsize = 12)
plt.title('행정동별 소비 건수', fontsize = 20, position=(0.5, 1.05))
plt.xlabel('종로구                                               노원구', fontsize = 15)
plt.ylabel('소비건수', fontsize = 15)
plt.show()

plt.figure(figsize=(10, 7))
sns.barplot(card_dong.index, card_dong['POP'])
plt.axvline(x=16.5, color='r', linestyle='--')
plt.xticks(rotation=75, fontsize = 12)
plt.title('행정동별 유동인구', fontsize = 20, position=(0.5, 1.05))
plt.xlabel('종로구                                               노원구', fontsize = 15)
plt.ylabel('유동인구', fontsize = 15)
plt.show()

card_max = card_outlier[card_outlier['MCT_CAT_CD'] == '요식업소(80)']
card_max = card_max.groupby(['GU_CD', 'DONG_CD', 'SEX_CD', 'AGE_CD']).sum()
card_max = card_max.reset_index(drop=False)
card_max = card_max.drop(['STD_DD', 'USE'], axis = 1)

def card_max_func(gu_cd, dong_cd):
    result = card_max[card_max['USE_AMT'] == max(card_max['USE_AMT'][(card_max['GU_CD'] == gu_cd) & (card_max['DONG_CD'] == dong_cd)])]
    result1 = dong_cd + ' 요식업소에서 가장 소비가 많은 층은 ' + result['SEX_CD'].iloc[0] + ' ' + result['AGE_CD'].iloc[0] + '이다.'
    result2 = round(100 * (max(card_max['USE_AMT'][(card_max['GU_CD'] == gu_cd) & (card_max['DONG_CD'] == dong_cd)]) / card_max['USE_AMT'][(card_max['GU_CD'] == gu_cd) & (card_max['DONG_CD'] == dong_cd)].sum()), 2)
    
    return result1, result2

for i in range(0, len(jongno_name)):
    print(card_max_func('종로구', jongno_name[i]))

for i in range(0, len(nowon_name)):
    print(card_max_func('노원구', nowon_name[i]))

df.to_csv('df.csv', index=False)
