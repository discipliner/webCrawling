from pcconfig import config

import pynecone as pc

# !/usr/bin/env python
# coding: utf-8


########################################################################################################################


# In[1]:

import json
from pandas.io.json import json_normalize
import warnings
import pandas as pd  # 데이터 분석을 위한 전처리를 위해 import 한다.
import matplotlib as mpl  # matplolib에서 음수 데이터의 '-'부호가 깨지는 것을 방지하기위해 import 한다.
import matplotlib.pyplot as plt  # 시각화를 하기 위해 import 한다.
import seaborn as sns
import os
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

warnings.filterwarnings(action='ignore')
mpl.rcParams['axes.unicode_minus'] = False  # matplolib에서 음수 데이터의 '-'부호가 깨지는 것을 방지한다.
pd.options.display.float_format = '{:,.5f}'.format
plt.rcParams["font.size"] = 10  # matplolib에서 사용할 글꼴 크기 설정
plt.rcParams["font.family"] = "D2Coding"  # matplolib에서 사용할 글꼴 설정

########################################################################################################################


# 상대경로 접근을 위해 디렉토리를 저장한다. (webapp → 'workspace/'에 이동 후 path에 저장 → webapp 복귀)
os.chdir('../')
path = os.getcwd()
print(path)
os.chdir('webapp/')
filename = f"{config.app_name}/{config.app_name}.py"

########################################################################################################################


# In[2]:

rank = pd.read_csv(path + '/data/rank.csv')
rank_final = pd.read_csv(path + '/data/rank_final - changed.csv')

# In[3]:

characterNamesEn = pd.read_csv(path + '/data/characterList - origin.csv')  # 캐릭터 영문명
characterNamesKr = pd.read_csv(path + '/data/characterList - changed.csv')  # 캐릭터 한글명
skinNames = pd.read_csv(path + '/data/skin - changed.csv')  # 스킨
weaponNames = pd.read_csv(path + '/data/weapon - changed.csv')  # 무기
armorNames = pd.read_csv(path + '/data/armor - changed.csv')  # 방어구
# 무기별 사용캐릭터 추가
weapon = pd.DataFrame({'num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25],
                       'name': ["글러브", "톤파", "방망이", "채찍", "투척", "암기", "활", "석궁", "권총", "돌격소총", "저격총", "망치", "도끼", "단검",
                                "양손검", "쌍검", "창", "쌍절곤", "레이피어", "기타", "카메라", "아르카나", "VF의수"],
                       'character': [['현우', '레온', '얀', '니키', '리다이린'], ['현우', '레온', '얀', '아이작', '알렉스'],
                                     ['바바라', '매그너스', '루크', '띠아'], ['레녹스', '마이', '라우라'],
                                     ['시셀라', '이바', '이렘', '아드리아나', '윌리엄', '자히르', '셀린'],
                                     ['시셀라', '엠마', '자히르', '타지아', '클로에', '혜진', '알렉스'],
                                     ['리오', '나딘', '혜진'], ['나딘', '칼라'], ['아야', '로지', '제니', '아이솔', '실비아', '알렉스'],
                                     ['아야', '아이솔', '헤이즈'],
                                     ['아야', '버니스', '테오도르'], ['매그너스', '수아', '일레븐'], ['재키', '마커스', '에스텔'],
                                     ['재키', '쇼이치', '캐시', '다니엘', '쇼우'],
                                     ['재키', '유키', '피오라', '에이든', '알렉스'], ['재키', '카밀로', '유키', '캐시'], ['쇼우', '펠릭스', '피오라'],
                                     ['리다이린', '피올로'],
                                     ['피오라', '키아라', '카밀로', '아델라', '엘레나'], ['하트', '프리야'], ['나타폰', '마르티나'],
                                     ['요한', '비앙카', '엠마', '아디나'], ['에키온']]})

# In[4]:

characterList = pd.DataFrame()

for i in range(len(rank_final.nameW.value_counts())):
    gg = f'{"{"}"nameW": "{rank_final.nameW.value_counts().index[i]}", ' \
         f'"code": {rank_final[rank_final.nameW == rank_final.nameW.value_counts().index[i]].characterNum.values[0]}{"}"}'

    characterList = pd.concat([characterList, json_normalize(json.loads(gg))], ignore_index=True)
characterList = characterList.sort_values('code')
characterList = characterList.reset_index(drop=True)
# characterList


# In[5]:

# 62개 캐릭터의 핵심 정보

df_code = pd.DataFrame()
df_characterStats = pd.DataFrame()

for i in range(84):
    character = pd.concat([df_code, rank_final[rank_final.nameW == characterList.nameW[i]]])
    stat = (
        # 실험체 이름
        f'{"{"}"characterName": "{characterList.nameW[i]}", '
        # 실험체 번호
        f'"characterCode": {characterList.code[i]}, '
        # 가장 많이 사용한 스킨, 사용 횟수
        f'"mostSkin": "{skinNames[skinNames.code == int(character.skinCode.value_counts().head(1).index[0])].values[0][0]}", '
        f'"mostSkinCount": {character.skinCode.value_counts().head(1).values[0]}, '

        # 무기(이대로 사용하면 가장 많이 사용한 무기로 나머지 무기도 통합됨)
        f'"characterWeapon": "{weapon[weapon.num == character.bestWeapon.values[0]].name.values[0]}",'

        # 여기부터 마지막까지 아래와 같은 리스트형식으로 무기별 분류 필요
        #  ([ {무기군1: 킬수}, {무기군2 : 킬수} ...])
        #  ([ {무기군1: 루트무기}, {무기군2 : 루트무기} ...] )

        # 평균 플레이어 킬수
        f'"averageKillPlayer": {character.playerKill.mean():.2f}, '
        # 평균 플레이어 데미지
        f'"averageDamegeToPlayer": {character.damageToPlayer.mean():.2f}, '
        # 평균 야동 킬수
        f'"averageKillMonster": {character.monsterKill.mean():.2f}, '
        # 평균 야동 데미지
        f'"averageDamegeToMonster": {character.damageToMonster.mean():.2f}, '
        # 게임 플레이 수
        f'"totalGames": {character.count()[0]}, '
        # # 평균 승률 => 자히르 투척 승률 0%짜리 터짐
        f'"winRate": {character[character.victory == 1].victory.count() / character.victory.count():.2f}, '

        # 평균 등수
        f'"averageRank": {character[character.escapeState != 3].gameRank.mean():.2f}, '
        # 탈출 횟수
        f'"escapeCount": {character[character.escapeState == 3].escapeState.count()}, '
        # 평균 mmr 획득률
        f'"averageMMR": {character.mmrGain.mean():.2f}, '
        # 픽률
        f'"pickRate": {character.count()[0] / 19248 * 100:.2f},'


        # 최종 아이템, 사용 횟수
        f'"finalWeapon": "{weaponNames[weaponNames.code == int(character["equipment.0"].value_counts().head(1).index[0])].values[0][1]}", '
        f'"finalWeaponCount": {character["equipment.0"].value_counts().head(1).values[0]}, '
        f'"finalBody": "{armorNames[armorNames.code == int(character["equipment.1"].value_counts().head(1).index[0])].values[0][1]}", '
        f'"finalBodyCount": {character["equipment.1"].value_counts().head(1).values[0]}, '
        f'"finalHead": "{armorNames[armorNames.code == int(character["equipment.2"].value_counts().head(1).index[0])].values[0][1]}", '
        f'"finalHeadCount": {character["equipment.2"].value_counts().head(1).values[0]}, '
        f'"finalArm": "{armorNames[armorNames.code == int(character["equipment.3"].value_counts().head(1).index[0])].values[0][1]}", '
        f'"finalArmCount": {character["equipment.3"].value_counts().head(1).values[0]}, '
        f'"finalFoot": "{armorNames[armorNames.code == int(character["equipment.4"].value_counts().head(1).index[0])].values[0][1]}", '
        f'"finalFootCount": {character["equipment.4"].value_counts().head(1).values[0]}, '
        f'"finalTinkled": "{armorNames[armorNames.code == int(character["equipment.5"].value_counts().head(1).index[0])].values[0][1]}", '
        f'"finalTinkledCount": {character["equipment.5"].value_counts().head(1).values[0]}, '

        # 가장 많이 선택한 루트 아이템, 사용 횟수
        f'"routeWeapon": "{weaponNames[weaponNames.code == int(character["equipFirstItemForLog.0"].value_counts().head(1).index[0][1:-1])].values[0][1]}", '
        f'"routeWeaponCount": {character["equipFirstItemForLog.0"].value_counts().head(1)[0]}, '
        f'"routeBody": "{armorNames[armorNames.code == int(character["equipFirstItemForLog.1"].value_counts().head(1).index[0][1:-1])].values[0][1]}", '
        f'"routeBodyCount": {character["equipFirstItemForLog.1"].value_counts().head(1)[0]}, '
        f'"routeHead": "{armorNames[armorNames.code == int(character["equipFirstItemForLog.2"].value_counts().head(1).index[0][1:-1])].values[0][1]}", '
        f'"routeHeadCount": {character["equipFirstItemForLog.2"].value_counts().head(1)[0]}, '
        f'"routeArm": "{armorNames[armorNames.code == int(character["equipFirstItemForLog.3"].value_counts().head(1).index[0][1:-1])].values[0][1]}", '
        f'"routeArmCount": {character["equipFirstItemForLog.3"].value_counts().head(1)[0]}, '
        f'"routeFoot": "{armorNames[armorNames.code == int(character["equipFirstItemForLog.4"].value_counts().head(1).index[0][1:-1])].values[0][1]}", '
        f'"routeFootCount": {character["equipFirstItemForLog.4"].value_counts().head(1)[0]}, '

        f'"routeTinkled": "", "routeTinkledCount": ""{"}"}'
    )
    df_characterStats = pd.concat([df_characterStats, json_normalize(json.loads(stat))], ignore_index=True)
    del character, stat
# df_characterStats


# In[6]:

df_characterStats.characterName[45] = '알렉스'
# print(df_characterStats.characterName[45])
characterList.nameW[45] = '알렉스'
# print(characterList.nameW[45])


# In[7]:

# 추가 필요!!!!!!!!
df_characterStats.loc[df_characterStats.characterName == '알렉스', 'characterWeapon'] = '톤파, 암기, 양손검, 권총'
# df_characterStats[df_characterStats.characterName=='알렉스'].characterWeapon

# 1-1
mmr = df_characterStats.averageMMR.mean()
pick = df_characterStats.pickRate.mean()
xy = pd.DataFrame()
for i, char in df_characterStats.iterrows():
    xy = pd.concat([xy, json_normalize(json.loads(
        f'{"{"}"characterCode": {characterList[characterList.nameW == char.characterName].code.values[0]}, '
        f'"characterName": "{characterList[characterList.nameW == char.characterName].nameW.values[0]}", '
        f'"pickRate": {df_characterStats.totalGames[i] / 19247 * 100:.2f}, "mmrGain": {df_characterStats.averageMMR[i]:.2f}{"}"}'))],
                   ignore_index=True)

########################################################################################################################


# 스타일 정의
style = {
    "font_family": "D2Coding",
    "font_size": "16px",
    pc.Center: {
        "padding_top": "10%",
    },
    pc.Vstack: {
        "spacing": "1.5em",
        "font_size": "1.5em",
    },
    pc.Hstack: {
        "spacing": "1.5em",
        "font_size": "1.5em",
    },
    pc.Heading: {
        "font_size": "2em",
    },
    pc.Box: {
        "font_size": "1.5em",
    },
    pc.Link: {
        "padding": "0.5em",
        "border": "0.1em solid",
        "border_radius": "1em",
        "box_sizing": "border-box",
        "color": "white",
        "_hover": {
            "color": "rgb(107,99,246)",
            "opacity": 0.85
        }
    },
    pc.Button: {
        "padding": "0.5em",
        "border": "0.1em solid",
        "border_radius": "1em",
        "box_sizing": "border-box",
        "color": "white",
        "_hover": {
            "color": "rgb(107,99,246)",
            "opacity": 0.85
        }
    },
    pc.Text: {
        "font_size": "0.7em"
    },
    pc.Tr: {
        "font_size": "1.5em",
    },
    pc.Td: {
        "font_size": "0.7em",
    }
}


########################################################################################################################


# State 클래스 정의
class State(pc.State):

    # In[8]:
    # 산점도 출력
    def squad_1_1(self):
        print('squad_1_1() 실행')
        plt.figure(figsize=(20, 12))
        plt.xlabel('픽률', fontsize=20)
        plt.ylabel('평균 MMR 획득', fontsize=20)
        # plt.scatter(xy.pickRate, xy.mmrGain)
        sns.scatterplot(xy, x=xy.pickRate, y=xy.mmrGain, hue=xy.characterName, legend=False)
        plt.title('Season8(0.75a patch) 스쿼드(랭크) 사분면', fontsize=20)
        plt.axhline(mmr, 0, 1)
        plt.axvline(pick, 0, 1)
        plt.axvline(pick * 2, 0, 1, linestyle='--', color='crimson')
        for _, j in xy.iterrows():
            plt.annotate(j.characterName,
                         (j.pickRate, j.mmrGain),
                         textcoords="offset points",  # 텍스트 위치를 (x,y)로 부터의 오프셋 (offset_x, offset_y)로 지정
                         xytext=(0, -15),  # (x, y)로 부터의 오프셋 (offset_x, offset_y)
                         ha='center')
        plt.show()

    # 1-2 프로필 이미지 산점도 출력
    def squad_1_2(self):
        global image
        print('squad_1_2() 실행')
        xy = pd.DataFrame()
        for i, char in df_characterStats.iterrows():
            xy = pd.concat([xy, json_normalize(json.loads(
                f'{"{"}"characterCode" : {characterList[characterList.nameW == char.characterName].code.values[0]} ,"characterName" : "{characterList[characterList.nameW == char.characterName].nameW.values[0]}" ,"pickRate" : {df_characterStats.totalGames[i] / 19247 * 100:.2f}, "mmrGain" : {df_characterStats.averageMMR[i]:.2f}{"}"}'))],
                           ignore_index=True)
        # 1-2-1
        face = []
        for i in range(len(df_characterStats)):
            face.append(f'{path}/data/mostSkin/{i}/mini.png')

        graphData = pd.DataFrame({'characterName': xy.characterName,
                                  'x': xy.pickRate,
                                  'y': xy.mmrGain,
                                  'image': face,
                                  })
        # 1-2-2
        plt.style.use(style='ggplot')
        plt.rcParams['figure.figsize'] = (22, 14)
        (fig, ax) = plt.subplots()
        plt.axhline(mmr, 0, 1, color='blue')
        plt.axvline(pick, 0, 1, color='blue')
        plt.axvline(pick * 2, 0, 1, linestyle='--', color='crimson')
        for x, y, image_path, characterName in zip(graphData.x, graphData.y, graphData.image, graphData.characterName):
            if ax is None:
                ax = plt.gca()
            try:
                image = plt.imread(image_path)
            except TypeError:
                pass
            im = OffsetImage(image, zoom=0.2)
            x, y = np.atleast_1d(x, y)
            artists = []
            for x0, y0 in zip(x, y):
                ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
                artists.append(ax.add_artist(ab))
            ax.update_datalim(np.column_stack([x, y]))
            ax.autoscale()
            # ax.annotate(characterName, (x, y), textcoords="offset points", xytext=(0, -25), ha='center') # 텍스트 출력
        plt.title('Season8(0.75a patch) 스쿼드(랭크) 사분면', fontsize=20)
        plt.xlabel('픽률', fontsize=20)
        plt.ylabel('평균 MMR 획득', fontsize=20)
        plt.show()

    # 실험체 검색 변수
    searchChar: str = ''
    searchWeapon: str = ''
    searchPick: float = 0.0
    searchMeanPick: float = 0.0
    searchWin: float = 0.0
    searchMmr: float = 0.0
    searchMeanMmr: float = 0.0
    searchSkin: str = '-'
    searchMsg: str = ''
    searchImg: str = './character_default.png'

    # 2-2 실험체 검색
    def character_2_2(self) -> str:
        print('character_2_2() 실행')
        # 2-2
        # w = input('무기')
        n = self.searchChar
        w = self.searchWeapon
        try:
            skinList = pd.DataFrame()
            skinList = pd.concat([skinList, df_characterStats[
                df_characterStats.characterCode == characterNamesKr[characterNamesKr.name == n].code.values[0]]], ignore_index=True)
            gg = f'{n}({w})'
            if n == '알렉스':
                gg = '알렉스'
                skin = df_characterStats[df_characterStats.characterName == f'{n}'].index[0]
                self.searchImg = './mostSkin/' + str(skin) + '/full.png'
                # img = mpl.image.imread(
                #     f'{path}/data/mostSkin/{skin}/full.png')
                # plt.axis('off')
                # plt.imshow(img)
                self.searchMsg = '알렉스는 권총, 톤파, 암기, 양손검을 사용하는 실험체입니다.'
                print('알렉스는 설정상 모든 무기를 다루지만 인게임에서는 밸런스 문제로 권총, 톤파, 암기, 양손검을 사용하는 실험체입니다.')
                print()
                print(f'평균 MMR획득: {mmr:.2f}, 평균 픽률: {pick:.2f}%')
                print(
                    f'{df_characterStats[df_characterStats.characterName == gg].characterName.values[0]} 픽률: {df_characterStats[df_characterStats.characterName == gg].pickRate.values[0]}%, 승률: {df_characterStats[df_characterStats.characterName == gg].winRate.values[0]}%, 평균 MMR획득: {df_characterStats[df_characterStats.characterName == gg].averageMMR.values[0]}, 모스트 스킨: {df_characterStats[df_characterStats.characterName == gg].mostSkin.values[0]}')
            elif w in skinList.characterWeapon.values:
                skin = df_characterStats[df_characterStats.characterName == f'{n}({w})'].index[0]
                self.searchImg = './mostSkin/' + str(skin) + '/full.png'
                # img = mpl.image.imread(f'{path}/data/mostSkin/{skin}/full.png')
                # plt.axis('off')
                # plt.imshow(img)
                print(f'평균 MMR획득: {mmr:.2f}, 평균 픽률: {pick:.2f}%')
                print(
                    f'{df_characterStats[df_characterStats.characterName == gg].characterName.values[0]} 픽률: {df_characterStats[df_characterStats.characterName == gg].pickRate.values[0]}%, 승률: {df_characterStats[df_characterStats.characterName == gg].winRate.values[0]}%, 평균 MMR획득: {df_characterStats[df_characterStats.characterName == gg].averageMMR.values[0]}, 모스트 스킨: {df_characterStats[df_characterStats.characterName == gg].mostSkin.values[0]}')
                self.searchMsg = ''
            else:
                print('else')
                print(f'{n}는(은) {w}를 사용하지 않는 실험체입니다.')
            self.searchPick = df_characterStats[df_characterStats.characterName == gg].pickRate.values[0]
            self.searchWin = df_characterStats[df_characterStats.characterName == gg].winRate.values[0] * 100
            self.searchMmr = df_characterStats[df_characterStats.characterName == gg].averageMMR.values[0]
            self.searchSkin = df_characterStats[df_characterStats.characterName == gg].mostSkin.values[0]
        except:
            print('except')
            # self.searchChar = ''
            # self.searchWeapon = ''
            self.searchPick = 0.0
            self.searchMeanPick = 0.0
            self.searchWin = 0.0
            self.searchMmr = 0.0
            self.searchMeanMmr = 0.0
            self.searchSkin = '-'
            self.searchMsg = n + '은(는) ' + w + '를 사용하지 않는 실험체입니다.'
            self.searchImg = './character_default.png'

    # 3 무기군
    def weapon_3_1(self):
        print('weapon_3_1() 실행')
        # 3-0
        df2 = pd.DataFrame()
        df_weaponStats = pd.DataFrame()

        for i in range(23):
            test = pd.concat([df2, rank_final[rank_final.bestWeapon == weapon.num[i]]])
            stat = (
                f'{"{"}"weaponName" : "{weapon.name[i]}", '
                f'"weaponCode" : {weapon.num[i]}, '
                # 평균 플레이어 킬수
                f'"averageKillPlayer" : {test.playerKill.mean():.2f}, '
                # 평균 플레이어 데미지
                f'"averageDamegeToPlayer" : {test.damageToPlayer.mean():.2f}, '
                # 평균 야동 킬수
                f'"averageKillMonster" : {test.monsterKill.mean():.2f}, '
                # 평균 야동 데미지
                f'"averageDamegeToMonster" : {test.damageToMonster.mean():.2f}, '
                # 게임 플레이 수
                f'"totalGames" : {test.count()[0]}, '
                # # 평균 승률 => 자히르 투척 승률 0%짜리 터짐
                f'"winRate" : {test[test.victory == 1].victory.count() / test.victory.count():.2f}, '
        
                # 평균 등수
                f'"averageRank" : {test[test.escapeState != 3].gameRank.mean():.2f}, '
                # 탈출 횟수
                f'"escapeCount" : {test[test.escapeState == 3].escapeState.count()}, '
                # 평균 mmr 획득률
                f'"averageMMR" : {test.mmrGain.mean():.2f}, '
                # 픽률
                f'"pickRate" : {test.count()[0] / 19248 * 100:.2f},'
        
        
                # 최종 아이템, 사용 횟수
                f'"finalWeapon" : "{weaponNames[weaponNames.code == int(test["equipment.0"].value_counts().head(1).index[0])].values[0][1]}", "finalWeaponCount" : {test["equipment.0"].value_counts().head(1).values[0]}, '
                f'"finalBody" : "{armorNames[armorNames.code == int(test["equipment.1"].value_counts().head(1).index[0])].values[0][1]}", "finalBodyCount" : {test["equipment.1"].value_counts().head(1).values[0]}, '
                f'"finalHead" : "{armorNames[armorNames.code == int(test["equipment.2"].value_counts().head(1).index[0])].values[0][1]}", "finalHeadCount" : {test["equipment.2"].value_counts().head(1).values[0]}, '
                f'"finalArm" : "{armorNames[armorNames.code == int(test["equipment.3"].value_counts().head(1).index[0])].values[0][1]}", "finalArmCount" : {test["equipment.3"].value_counts().head(1).values[0]}, '
                f'"finalFoot" : "{armorNames[armorNames.code == int(test["equipment.4"].value_counts().head(1).index[0])].values[0][1]}", "finalFootCount" : {test["equipment.4"].value_counts().head(1).values[0]}, '
                f'"finalTinkled" : "{armorNames[armorNames.code == int(test["equipment.5"].value_counts().head(1).index[0])].values[0][1]}", "finalTinkledCount" : {test["equipment.5"].value_counts().head(1).values[0]}, '
        
                # 가장 많이 선택한 루트 아이템, 사용 횟수
                f'"routeWeapon" : "{weaponNames[weaponNames.code == int(test["equipFirstItemForLog.0"].value_counts().head(1).index[0][1:-1])].values[0][1]}", "routeWeaponCount" : {test["equipFirstItemForLog.0"].value_counts().head(1)[0]}, '
                f'"routeBody" : "{armorNames[armorNames.code == int(test["equipFirstItemForLog.1"].value_counts().head(1).index[0][1:-1])].values[0][1]}", "routeBodyCount" : {test["equipFirstItemForLog.1"].value_counts().head(1)[0]}, '
                f'"routeHead" : "{armorNames[armorNames.code == int(test["equipFirstItemForLog.2"].value_counts().head(1).index[0][1:-1])].values[0][1]}", "routeHeadCount" : {test["equipFirstItemForLog.2"].value_counts().head(1)[0]}, '
                f'"routeArm" : "{armorNames[armorNames.code == int(test["equipFirstItemForLog.3"].value_counts().head(1).index[0][1:-1])].values[0][1]}", "routeArmCount" : {test["equipFirstItemForLog.3"].value_counts().head(1)[0]}, '
                f'"routeFoot" : "{armorNames[armorNames.code == int(test["equipFirstItemForLog.4"].value_counts().head(1).index[0][1:-1])].values[0][1]}", "routeFootCount" : {test["equipFirstItemForLog.4"].value_counts().head(1)[0]}, '
        
                f'"routeTinkled" : "", "routeTinkledCount" : ""{"}"}'
            )
            df_weaponStats = pd.concat([df_weaponStats, json_normalize(json.loads(stat))], ignore_index=True)
            del test, stat

        # 3-1
        plt.figure(figsize=[10, 6])
        wmmr = df_weaponStats.averageMMR.mean()
        wpick = df_weaponStats.pickRate.mean()
        gg = pd.DataFrame()
        for i, char in df_weaponStats.iterrows():
            gg = pd.concat([gg, json_normalize(json.loads(
                f'{"{"}"weaponCode" : {weapon[weapon.name == char.weaponName].num.values[0]} ,"weaponName" : "{weapon[weapon.name == char.weaponName].name.values[0]}" ,"pickRate" : {df_weaponStats[df_weaponStats.weaponName == weapon[weapon.name == char.weaponName].name.values[0]].totalGames[i] / 19247 * 100:.2f}, "mmrGain" : {df_weaponStats[df_weaponStats.weaponName == weapon[weapon.name == char.weaponName].name.values[0]].averageMMR[i]:.2f}{"}"}'))])
        plt.xlabel('픽률', fontsize=20)
        plt.ylabel('평균 MMR 획득', fontsize=20)
        # plt.scatter(xy.pickRate, xy.mmrGain)
        sns.scatterplot(gg, x=gg.pickRate, y=gg.mmrGain, hue=gg.weaponName, legend=False)
        plt.title('Season8(0.75a patch) 스쿼드(랭크, 무기군) 사분면', fontsize=20)
        plt.axhline(wmmr, 0, 1, color='blue')
        plt.axvline(wpick, 0, 1, color='blue')
        for _, j in gg.iterrows():
            plt.annotate(j.weaponName,
                         (j.pickRate, j.mmrGain),
                         textcoords="offset points",  # 텍스트 위치를 (x,y)로 부터의 오프셋 (offset_x, offset_y)로 지정
                         xytext=(0, -15),  # (x, y)로 부터의 오프셋 (offset_x, offset_y)
                         ha='center')
        plt.show()

    classifyWeapon: str = ''
    classifyMsg: str = ''

    def weapon_3_2_1(self):
        # 3-2-0 무기군 검색
        # w = input('검색할 무기군')
        self.classifyMsg = ''
        w = self.classifyWeapon
        xyw = pd.DataFrame()
        try:
            for i, char in df_characterStats.iterrows():
                if char.characterWeapon == w:
                    xyw = pd.concat([xyw, json_normalize(json.loads(f'{"{"}"characterCode" : {char.characterCode} '
                                                                    f',"characterName" : "{char.characterName}" '
                                                                    f',"pickRate" : {df_characterStats[df_characterStats.characterWeapon == w].totalGames[i] / 19247 * 100:.2f}, '
                                                                    f'"mmrGain" : {df_characterStats[df_characterStats.characterWeapon == w].averageMMR[i]:.2f}{"}"}'))],
                                    ignore_index=True)

            if w in ['권총', '양손검', '암기', '톤파']:
                xyw = pd.concat([xyw, json_normalize(json.loads(
                    f'{"{"}"characterCode" : {df_characterStats[df_characterStats.characterName == "알렉스"].characterCode.values[0]} '
                    f',"characterName" : "{df_characterStats[df_characterStats.characterName == "알렉스"].characterName.values[0]}"'
                    f',"pickRate" : {df_characterStats[df_characterStats.characterName == "알렉스"].totalGames.values[0] / 19247 * 100:.2f},'
                    f'"mmrGain" : {df_characterStats[df_characterStats.characterName == "알렉스"].averageMMR.values[0]:.2f}{"}"}'))],
                                ignore_index=True)
            face = []
            if w not in weapon.name.values:
                print(f'{w}은(는) 존재하지 않는 무기군입니다.')
                self.classifyMsg = w + '은(는) 존재하지 않는 무기군입니다.'
            else:
                for i in range(len(xyw)):
                    face.append(
                        f'{path}/data/mostSkin/{df_characterStats[df_characterStats.characterName == xyw.characterName[i]].index[0]}/mini.png')

                wgraphData = pd.DataFrame({'characterName': xyw.characterName,
                                           'x': xyw.pickRate,
                                           'y': xyw.mmrGain,
                                           'image': face,
                                           })
                print(wgraphData)
                # 3-2-1
                plt.figure(figsize=(10, 6))
                plt.xlabel('픽률', fontsize=20)
                plt.ylabel('평균 MMR 획득', fontsize=20)
                sns.scatterplot(xyw, x=xyw.pickRate, y=xyw.mmrGain, hue=xyw.characterName, legend=False)
                plt.title(f'Season8(0.75a patch) 무기군<{w}>(스쿼드, 랭크) 사분면', fontsize=20)
                plt.axhline(mmr, 0, 1, color='blue')
                plt.axvline(pick, 0, 1, color='blue')
                plt.axvline(pick * 2, 0, 1, linestyle='--', color='crimson')
                for _, j in xyw.iterrows():
                    plt.annotate(j.characterName,
                                 (j.pickRate, j.mmrGain),
                                 textcoords="offset points",  # 텍스트 위치를 (x,y)로 부터의 오프셋 (offset_x, offset_y)로 지정
                                 xytext=(0, -15),  # (x, y)로 부터의 오프셋 (offset_x, offset_y)
                                 ha='center')
                plt.show()
        except:
            self.classifyMsg = w + '은(는) 존재하지 않는 무기군입니다.'

    def weapon_3_2_2(self):
        # 3-2-0 무기군 검색
        # w = input('검색할 무기군')
        self.classifyMsg = ''
        w = self.classifyWeapon
        xyw = pd.DataFrame()
        try:
            for i, char in df_characterStats.iterrows():
                if char.characterWeapon == w:
                    xyw = pd.concat([xyw, json_normalize(json.loads(f'{"{"}"characterCode" : {char.characterCode} '
                                                                    f',"characterName" : "{char.characterName}" '
                                                                    f',"pickRate" : {df_characterStats[df_characterStats.characterWeapon == w].totalGames[i] / 19247 * 100:.2f}, '
                                                                    f'"mmrGain" : {df_characterStats[df_characterStats.characterWeapon == w].averageMMR[i]:.2f}{"}"}'))],
                                    ignore_index=True)

            if w in ['권총', '양손검', '암기', '톤파']:
                xyw = pd.concat([xyw, json_normalize(json.loads(
                    f'{"{"}"characterCode" : {df_characterStats[df_characterStats.characterName == "알렉스"].characterCode.values[0]} '
                    f',"characterName" : "{df_characterStats[df_characterStats.characterName == "알렉스"].characterName.values[0]}"'
                    f',"pickRate" : {df_characterStats[df_characterStats.characterName == "알렉스"].totalGames.values[0] / 19247 * 100:.2f},'
                    f'"mmrGain" : {df_characterStats[df_characterStats.characterName == "알렉스"].averageMMR.values[0]:.2f}{"}"}'))],
                                ignore_index=True)
            face = []
            if w not in weapon.name.values:
                print(f'{w}은(는) 존재하지 않는 무기군입니다.')
                self.classifyMsg = w + '은(는) 존재하지 않는 무기군입니다.'
            else:
                for i in range(len(xyw)):
                    face.append(
                        f'{path}/data/mostSkin/{df_characterStats[df_characterStats.characterName == xyw.characterName[i]].index[0]}/mini.png')

                wgraphData = pd.DataFrame({'characterName': xyw.characterName,
                                           'x': xyw.pickRate,
                                           'y': xyw.mmrGain,
                                           'image': face,
                                           })
                print(wgraphData)
                # 3-2-2
                plt.style.use(style='ggplot')
                # plt.figure(figsize=(22, 14))
                plt.rcParams['figure.figsize'] = (10, 6)

                fig, ax = plt.subplots()
                plt.axhline(mmr, 0, 1, color='blue')
                plt.axvline(pick, 0, 1, color='blue')
                plt.axvline(pick * 2, 0, 1, linestyle='--', color='crimson')
                for x, y, image_path, characterName in zip(wgraphData.x, wgraphData.y, wgraphData.image, wgraphData.characterName):
                    if ax is None:
                        ax = plt.gca()
                    try:
                        image = plt.imread(image_path)
                    except TypeError:
                        pass
                    im = OffsetImage(image, zoom=0.2)
                    x, y = np.atleast_1d(x, y)
                    artists = []
                    for x0, y0 in zip(x, y):
                        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
                        artists.append(ax.add_artist(ab))
                    ax.update_datalim(np.column_stack([x, y]))
                    ax.autoscale()
                    # ax.annotate(characterName, (x, y), textcoords="offset points", xytext=(0, -25), ha='center') # 텍스트 출력
                plt.title(f'Season8(0.75a patch) 무기군<{w}>(스쿼드, 랭크) 사분면', fontsize=20)
                plt.xlabel('픽률', fontsize=20)
                plt.ylabel('평균 MMR 획득', fontsize=20)
                plt.show()
        except:
            self.classifyMsg = w + '은(는) 존재하지 않는 무기군입니다.'


########################################################################################################################


# 인덱스 페이지
def index_0():
    print('index() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("ER 웹 크롤링 및 데이터 분석"),
            # pc.box("Progress: editing ", pc.code(filename, font_size="1em")),
            pc.image(src='./index.png'),
            pc.hstack(
                pc.link(
                    "스쿼드",
                    href='/squad',
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "실험체",
                    href='/character',
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "무기군",
                    href='/weapon',
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                )
            ),
            pc.box(''),
            pc.link(
                "시즌 요약",
                href='/fin',
                box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                background='red',
                width='6em',
                align='middle'
            )
        ),
    )


########################################################################################################################


# 스쿼드 페이지
def squad_1():
    print('squad() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("Season8 스쿼드(랭크) 사분면"),
            pc.image(src='./squad_default.png'),
            pc.box(""),
            pc.hstack(
                pc.link(
                    "Scatter",
                    href='#',
                    on_click=State.squad_1_1,
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Profile",
                    href='#',
                    on_click=State.squad_1_2,
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Home",
                    href='/',
                    background='red'
                )
            )
        )
    )


########################################################################################################################


# 실험체 페이지
def character_2():
    print('character() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("Season8 실험체 검색"),
            # pc.image(src='./character_default.png'),
            pc.image(src=State.searchImg),
            pc.box("실험체 정보"),
            pc.hstack(
                pc.text("실험체명"),
                pc.input(
                    on_blur=State.set_searchChar,
                    placeholder="Type Character",
                    width="160px"
                )
            ),
            pc.hstack(
                pc.text("사용무기"),
                pc.input(
                    on_blur=State.set_searchWeapon,
                    placeholder="Type Weapon",
                    width="160px"
                )
            ),
            pc.box(""),
            pc.table_container(
                pc.table(
                    pc.thead(
                        pc.tr(
                            pc.th("픽률(%)"),
                            pc.th("승률(%)"),
                            pc.th("평균 MMR 획득"),
                            pc.th("모스트 스킨")
                        )
                    ),
                    pc.tbody(
                        pc.tr(
                            pc.td(State.searchPick, '%'),
                            pc.td(State.searchWin, '%'),
                            pc.td(State.searchMmr),
                            pc.td(State.searchSkin)
                        )
                    ),
                    font_size="20",
                    width="700px"
                ),
            ),
            pc.box(""),
            pc.text(State.searchMsg),
            pc.hstack(
                pc.link(
                    "Search",
                    href='#',
                    on_click=State.character_2_2,
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Home",
                    href='/',
                    background='red'
                )
            )
        )
    )


########################################################################################################################


# 무기군 페이지
def weapon_3():
    print('weapon() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("Season8 무기군 분류"),
            pc.image(src='weapon_default.png'),
            pc.box(""),
            # pc.box("무기군 검색"),
            pc.hstack(
                pc.text("사용무기"),
                pc.input(
                    on_blur=State.set_classifyWeapon,
                    placeholder="Type Weapon",
                    width="160px"
                )
            ),
            pc.box(""),
            pc.text(State.classifyMsg),
            pc.hstack(
                pc.link(
                    "Scatter 1",
                    href='#',
                    on_click=State.weapon_3_1,
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Scatter 2",
                    href='#',
                    on_click=State.weapon_3_2_1,
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Profile",
                    href='#',
                    on_click=State.weapon_3_2_2,
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Home",
                    href='/',
                    background='red'
                )
            )
        )
    )


########################################################################################################################


# 시즌 8 요약 페이지
def fin_4():
    print('fin() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("<Season8 0.75a patch 요약>"),
            pc.image(src='./mostItem/metaGolem-half.png'),
            pc.box(""),
            pc.heading('※ 가장 많이 사용된 실험체 & 스킨 및 부위별 아이템', font_size='1.3em'),
            pc.box(""),
            # pc.box(f'실험체(스킨): {characterNamesKr[characterNamesKr.code == rank_final.characterNum.value_counts().head(1).index[0]].name.values[0]}({skinNames[skinNames.code == rank_final[rank_final.characterNum == rank_final.characterNum.value_counts().head(1).index[0]].skinCode.values[0]].values[0][0]})'),
            # pc.box(f'무기: {weaponNames[weaponNames.code == int(rank_final["equipFirstItemForLog.0"].value_counts().head(1).index[0][1:-1])].name.values[0]}, 옷: {armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.1"].value_counts().head(1).index[0][1:-1])].name.values[0]}'),
            # pc.box(f'머리: {armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.2"].value_counts().head(1).index[0][1:-1])].name.values[0]}, 팔: {armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.3"].value_counts().head(1).index[0][1:-1])].name.values[0]}'),
            # # 루트 장신구 api가 null이 뜨는 버그가 있어서 최종장신구로 대체
            # pc.box(f'다리: {armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.4"].value_counts().head(1).index[0][1:-1])].name.values[0]}, 장신구: {armorNames[armorNames.code == int(rank_final["equipment.5"].value_counts().head(1).index[0])].name.values[0]}'),
            pc.table_container(
                pc.table(
                    pc.thead(
                        pc.tr(
                            pc.th('실험체'),
                            pc.td(f'{characterNamesKr[characterNamesKr.code == rank_final.characterNum.value_counts().head(1).index[0]].name.values[0]}'),
                            pc.th('스킨'),
                            pc.td(f'{skinNames[skinNames.code == rank_final[rank_final.characterNum == rank_final.characterNum.value_counts().head(1).index[0]].skinCode.values[0]].values[0][0]}'),
                        )
                    ),
                    pc.tbody(
                        pc.tr(
                            pc.th('무기'),
                            pc.td(f'{weaponNames[weaponNames.code == int(rank_final["equipFirstItemForLog.0"].value_counts().head(1).index[0][1:-1])].name.values[0]}'),
                            pc.th('옷'),
                            pc.td(f'{armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.1"].value_counts().head(1).index[0][1:-1])].name.values[0]}')
                        ),
                        pc.tr(
                            pc.th('머리'),
                            pc.td(f'{armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.2"].value_counts().head(1).index[0][1:-1])].name.values[0]}'),
                            pc.th('팔'),
                            pc.td(f'{armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.3"].value_counts().head(1).index[0][1:-1])].name.values[0]}')
                        ),
                        pc.tr(
                            pc.th('다리'),
                            pc.td(f'{armorNames[armorNames.code == int(rank_final["equipFirstItemForLog.4"].value_counts().head(1).index[0][1:-1])].name.values[0]}'),
                            pc.th('장신구'),
                            pc.td(f'{armorNames[armorNames.code == int(rank_final["equipment.5"].value_counts().head(1).index[0])].name.values[0]}')
                        ),
                    ),
                    # font_size="1em",
                    width="700px"
                ),
            ),
            pc.box(""),
            pc.hstack(
                pc.link(
                    "Home",
                    href='/',
                    background='red'
                )
            )
        )
    )

########################################################################################################################


# 홈페이지 적용 및 컴파일
app = pc.App(state=State, style=style)
app.add_page(index_0, route='/', title='CRUNCH')
app.add_page(squad_1, route='/squad', title='CRUNCH')
app.add_page(character_2, route='/character', title='CRUNCH')
app.add_page(weapon_3, route='/weapon', title='CRUNCH')
app.add_page(fin_4, route='/fin', title='CRUNCH')
app.compile()
