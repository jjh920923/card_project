import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import font_manager, rc

# 작업 디렉토리 지정
os.chdir('C:\\Users\\Msi\\Desktop\\공모전\\카드소비 프로젝트\\데이터')

# seaborn을 사용하여 그릴 때 배경을 바꿔준다.
# 배경을 바꾸게 되면 폰트가 초기화되기 때문에 폰트를 설정하기 전에 미리 설정해주도록 한다.
sns.set_style('darkgrid')

# 한글 폰트가 깨지기 때문에 폰트를 바꿔준다.
font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
rc('font', family=font_name)

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

# 유동인구 데이터 변형 - PPT 16장 그림 1, 2
def pop_trans(file):
    df = pd.read_csv(file, sep="|")
    
    # 카드 데이터와 병합을 위해 20세 미만의 남녀 유동인구와 65세 이상의 남녀 유동인구를 만들어준다.
    df['MAN_FLOW_POP_CNT_20'] = df.iloc[:,3:8].sum(axis=1)
    df['MAN_FLOW_POP_CNT_65'] = df.iloc[:,17:19].sum(axis=1)
    df['WMAN_FLOW_POP_CNT_20'] = df.iloc[:,19:24].sum(axis=1)
    df['WMAN_FLOW_POP_CNT_65'] = df.iloc[:,32:34].sum(axis=1)

    # 병합에 쓰였던 데이터들의 모두 삭제한다.    
    df = df.drop(['STD_YM', 'HDONG_CD', 'MAN_FLOW_POP_CNT_0004', 'MAN_FLOW_POP_CNT_0509', 'MAN_FLOW_POP_CNT_1014', 'MAN_FLOW_POP_CNT_1519', 
                  'MAN_FLOW_POP_CNT_2024', 'MAN_FLOW_POP_CNT_6569', 'MAN_FLOW_POP_CNT_70U', 
                  'WMAN_FLOW_POP_CNT_0004', 'WMAN_FLOW_POP_CNT_0509', 'WMAN_FLOW_POP_CNT_1014', 'WMAN_FLOW_POP_CNT_1519', 
                  'WMAN_FLOW_POP_CNT_2024', 'WMAN_FLOW_POP_CNT_6569', 'WMAN_FLOW_POP_CNT_70U'], axis = 1)
    
    re_columns = list(df.columns[:2]) + sorted(df.columns[2:])
    df = df[re_columns]

    # 현재 컬럼명을 다시 알아보기 쉽게 바꿔준다.
    colums = ['STD_YMD','HDONG_NM',
              '남자 25세 미만','남자 25세~29세','남자 30세~34세','남자 35세~39세','남자 40세~44세',
              '남자 45세~49세','남자 50세~54세','남자 55세~59세','남자 60세~64세','남자 65세 이상',
              '여자 25세 미만','여자 25세~29세','여자 30세~34세','여자 35세~39세','여자 40세~44세',
              '여자 45세~49세','여자 50세~54세','여자 55세~59세','여자 60세~64세','여자 65세 이상']
    df.columns = colums
    
    p = df.iloc[:,:2]
    p = p.iloc[np.repeat(np.arange(len(p)), 20)]

    sex = (['남자']*10 + ['여자']*10)*df.shape[0]
    age = (age_name*2)*df.shape[0]

    p['SEX_CD'] = sex
    p['AGE_CD'] = age   

    p = p.reset_index(drop = True)

    p['POP'] = df.iloc[:,2:].stack().reset_index(drop = True)
    return p

# 생성한 함수로 18년 4월 ~ 19년 3월까지 유동인구 데이터 변형하기

file_name = ['1804','1805','1806','1807','1808','1809',
             '1810','1811','1812','1901','1902','1903']

for i in file_name:
    globals()['p'+i] = pop_trans('노원_종로_FLOW_AGE_20'+i+'.csv')

# 변형한 18년 4월 ~ 19년 3월까지의 유동인구 데이터 합치기
pop = pd.concat([p1804, p1805, p1806, p1807, p1808, p1809, p1810, p1811, p1812, p1901, p1902, p1903])
pop.rename(columns = {'STD_YMD' : 'STD_DD', 'HDONG_NM' : 'DONG_CD'}, inplace = True)

# 변형한 유동인구 데이터를 저장
pop.to_csv('pop.csv', index=False)
