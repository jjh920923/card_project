import os
import numpy as np
import pandas as pd
import seaborn as sns
import scikitplot as skplt
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import KFold, cross_val_score, train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_squared_error


# 작업 디렉토리 지정
os.chdir('C:\\Users\\Msi\\Desktop\\공모전\\카드소비 프로젝트\\데이터')

# seaborn을 사용하여 그릴 때 배경을 바꿔준다.
# 배경을 바꾸게 되면 폰트가 초기화되기 때문에 폰트를 설정하기 전에 미리 설정해주도록 한다.
sns.set_style('darkgrid')

# 한글 폰트가 깨지기 때문에 폰트를 바꿔준다.
font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
rc('font', family=font_name)

df = pd.read_csv('df.csv')

df.corr()

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

# 데이터 분포 확인 후 범주화 범위 설정하기
def category_EDA(column):
    sns.distplot(df[column])
    plt.title(str(column) + "의 데이터 분포도",  position=(0.5, 1.05), fontsize = 20)
    plt.show()
    
    print(df[column].describe())
    return

category_EDA("USE_CNT")
category_EDA("USE_AMT")
category_EDA("USE")
category_EDA("POP")

def category(column, level6):
    df[column] = pd.qcut(df[column][df[column] < level6], q = 5, labels = [1, 2, 3, 4, 5])
    df[column] = df[column].cat.add_categories(6)
    df[column].fillna(6, inplace = True)
    return

# 5000 이상 -> 6
category("USE_CNT", 5000)
# 100000 이상 -> 6
category("USE_AMT", 100000)
# 70 이상 -> 6
category("USE", 70)
# 20000 이상 -> 6
category("POP", 20000)

dummy_gu_dong = pd.get_dummies(df["DONG_CD"])
dummy_sex = pd.get_dummies(df["SEX_CD"])
dummy_age = pd.get_dummies(df["AGE_CD"])
dummy_week = pd.get_dummies(df["week"], prefix="week")
dummy_month = pd.get_dummies(df["month"], prefix="month")

df = pd.concat([df, dummy_gu_dong, dummy_sex, dummy_age, dummy_week, dummy_month], axis = 1)
df = df.drop(["STD_DD", "DONG_CD", "SEX_CD", "AGE_CD", "week", "month"], axis = 1)

final = df.copy()

x = final.drop(["USE_AMT"], axis = 1)
y = final["USE_AMT"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 5)


def analysis(model):
    model.fit(x_train, y_train)

    pred = model.predict(x_test)
    print(confusion_matrix(y_test, pred))
    accuracy_score(y_test, pred)
    print(classification_report(y_test, pred))

    pred_prob = model.predict_proba(x_test)
    skplt.metrics.plot_confusion_matrix(y_test, pred, normalize=True)
    skplt.metrics.plot_roc(y_test, pred_prob)
    score = round(model.score(x_test, y_test), 4)
    return {"accuracy" : score}



model = LogisticRegression(multi_class='multinomial', solver='newton-cg')
analysis(model)

model = LinearDiscriminantAnalysis()
analysis(model)

model = ExtraTreesClassifier()
analysis(model)

model = DecisionTreeClassifier()
analysis(model)

model = GaussianNB()
analysis(model)

model = KNeighborsClassifier()
analysis(model)

model = RandomForestClassifier()
analysis(model)

model = SVC()
analysis(model)


train_errors, test_errors = [], []
estimators = [1, 3, 5, 7, 10, 20, 30, 40, 50, 60, 70]
for estimator in estimators:
    model = RandomForestClassifier(n_estimators = estimator)
    model.fit(x_train, y_train)
    y_train_predict = model.predict(x_train)
    y_test_predict = model.predict(x_test)
    train_errors.append(mean_squared_error(y_train, y_train_predict))
    test_errors.append(mean_squared_error(y_test, y_test_predict))
    
plt.plot(estimators, np.sqrt(train_errors), 'r-+', linewidth=2, label='훈련 세트')
plt.plot(estimators, np.sqrt(test_errors), 'b-', linewidth=3, label='검증 세트')
plt.legend(loc="middle right", fontsize=14)
plt.title('estimator에 따른 RMSE', fontsize=17)
plt.xlabel("n of estimators", fontsize=14)
plt.ylabel("RMSE", fontsize=14)


# 그래프를 보고 훈련 데이터와 검증 데이터가 가까워지는 순간이 가장 적합한 모델이다.
# 두 차이가 점점 멀어지면 과적합으로 가는 과정이라고 볼 수 있다.
# 그래서 이 그래프는 depth 약 25에서 적합하다 판단이되고
# 0~10 사이에서는 언더피팅, 30 이후로는 오버피팅으로 가는 과정이라고 볼 수 있다.
train_errors_depth, test_errors_depth = [], []
max_depth = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105]
for depth in max_depth:
    model = RandomForestClassifier(max_depth=depth)
    model.fit(x_train, y_train)
    y_train_predict = model.predict(x_train)
    y_test_predict = model.predict(x_test)
    train_errors_depth.append(mean_squared_error(y_train, y_train_predict))
    test_errors_depth.append(mean_squared_error(y_test, y_test_predict))
    
plt.plot(max_depth, np.sqrt(train_errors_depth), 'r-+', linewidth=2, label='훈련 세트')
plt.plot(max_depth, np.sqrt(test_errors_depth), 'b-', linewidth=3, label='검증 세트')
plt.legend(loc="upper right", fontsize=14)
plt.title('depth에 따른 RMSE', fontsize=17)
plt.xlabel("depth", fontsize=14)
plt.ylabel("RMSE", fontsize=14)


train_errors_split, test_errors_split = [], []
min_samples_split = [2, 6, 10, 14, 18, 22, 26, 30, 34, 38]
for split in min_samples_split:
    model = RandomForestClassifier(min_samples_split=split)
    model.fit(x_train, y_train)
    y_train_predict = model.predict(x_train)
    y_test_predict = model.predict(x_test)
    train_errors_split.append(mean_squared_error(y_train, y_train_predict))
    test_errors_split.append(mean_squared_error(y_test, y_test_predict))
    
plt.plot(min_samples_split, np.sqrt(train_errors_split), 'r-+', linewidth=2, label='훈련 세트')
plt.plot(min_samples_split, np.sqrt(test_errors_split), 'b-', linewidth=3, label='검증 세트')
plt.legend(loc="lower right", fontsize=14)
plt.title('split에 따른 RMSE', fontsize=17)
plt.xlabel("n of split", fontsize=14)
plt.ylabel("RMSE", fontsize=14)


train_errors_leaf, test_errors_leaf = [], []
min_samples_leaf = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
for leaf in min_samples_leaf:
    model = RandomForestClassifier(min_samples_leaf=leaf)
    model.fit(x_train, y_train)
    y_train_predict = model.predict(x_train)
    y_test_predict = model.predict(x_test)
    train_errors_leaf.append(mean_squared_error(y_train, y_train_predict))
    test_errors_leaf.append(mean_squared_error(y_test, y_test_predict))
    
plt.plot(min_samples_leaf, np.sqrt(train_errors_leaf), 'r-+', linewidth=2, label='훈련 세트')
plt.plot(min_samples_leaf, np.sqrt(test_errors_leaf), 'b-', linewidth=3, label='검증 세트')
plt.legend(loc="lower right", fontsize=14)
plt.title('leaf에 따른 RMSE', fontsize=17)
plt.xlabel("leaf", fontsize=14)
plt.ylabel("RMSE", fontsize=14)


hyperRF = dict(max_depth=25, min_samples_split=20, min_samples_leaf=4)
model = RandomForestClassifier(**hyperRF)
analysis(model)


n_estimators = [1, 2, 3, 4, 5]
max_depth = [10, 15, 20, 25, 30]
min_samples_split = [5, 10, 15, 20, 25]
min_samples_leaf = [1, 2, 3, 4, 5] 

hyperRF = dict(n_estimators = n_estimators, max_depth = max_depth,  
               min_samples_split = min_samples_split, 
               min_samples_leaf = min_samples_leaf)

gridRF = GridSearchCV(model, hyperRF, error_score='accuracy', cv = 3, 
                      verbose = 1, n_jobs = -1)

gridRF.fit(x_train, y_train)

gridRF.best_params_


hyperRF = dict(n_estimators=5, max_depth=30, min_samples_split=25, min_samples_leaf=4)
model = RandomForestClassifier(**hyperRF)
analysis(model)