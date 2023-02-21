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
plt.rcParams["font.family"] = "NanumGothicCoding"  # matplolib에서 사용할 글꼴 설정


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

#0
df_characterStats.loc[df_characterStats.characterName == '알렉스', 'characterWeapon'] = '톤파, 암기, 양손검, 권총'
# df_characterStats[df_characterStats.characterName=='알렉스'].characterWeapon

mmr = df_characterStats.averageMMR.mean()
pick = df_characterStats.pickRate.mean()
xy = pd.DataFrame()
for i, char in df_characterStats.iterrows():
    xy = pd.concat([xy, json_normalize(json.loads(
        f'{"{"}"characterCode": {characterList[characterList.nameW == char.characterName].code.values[0]}, '
        f'"characterName": "{characterList[characterList.nameW == char.characterName].nameW.values[0]}", '
        f'"pickRate": {df_characterStats.totalGames[i] / 19247 * 100:.2f}, "mmrGain": {df_characterStats.averageMMR[i]:.2f}{"}"}'))], ignore_index=True)


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
        "font_size": "2em",
    },
    pc.Heading: {
        "font_size": "2em",
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
    }
}


########################################################################################################################


# State 클래스 정의
class State(pc.State):

    # In[8]:
    # 산점도 출력
    def scatter(self):
        print('scatter() 실행')
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

    # 프로필 이미지 산점도 출력
    def profile(self):
        global image
        print('profile() 실행')
        xy = pd.DataFrame()
        for i, char in df_characterStats.iterrows():
            xy = pd.concat([xy, json_normalize(json.loads(
                f'{"{"}"characterCode" : {characterList[characterList.nameW == char.characterName].code.values[0]} ,"characterName" : "{characterList[characterList.nameW == char.characterName].nameW.values[0]}" ,"pickRate" : {df_characterStats.totalGames[i] / 19247 * 100:.2f}, "mmrGain" : {df_characterStats.averageMMR[i]:.2f}{"}"}'))],
                           ignore_index=True)

        face = []
        for i in range(len(df_characterStats)):
            face.append(f'{path}/data/mostSkin/{i}/mini.png')

        graphData = pd.DataFrame({'characterName': xy.characterName,
                                  'x': xy.pickRate,
                                  'y': xy.mmrGain,
                                  'image': face,
                                  })
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

    # 실험체 검색
    searchChar: str = ''
    searchWeapon: str = ''
    '''c_name: list = []
    c_pickRate: list = []
    c_winRate: list = []
    c_mmr: list = []
    c_skin: list = []'''
    searchPick: float = 0.0
    searchWin: float = 0.0
    searchMmr: float = 0.0
    searchSkin: str = ''
    def search(self) -> str:
        print('search() 실행')
        '''# 2-1
        # n = input('검색할 실험체: ')
        n = self.searchChar
        img = mpl.image.imread(
            f'{path}/data/mostSkin/{df_characterStats[df_characterStats.characterCode == characterNamesKr[characterNamesKr.name == n].code.values[0]].index[0]}/full.png')
        plt.axis('off')
        plt.imshow(img)
        print(f'평균 MMR획득: {mmr:.2f}, 평균 픽률: {pick:.2f}%')
        self.c_name = []
        self.c_pickRate = []
        self.c_winRate = []
        self.c_mmr = []
        self.c_skin = []
        for _, c in df_characterStats.iterrows():
            if c.characterCode == characterNamesKr[characterNamesKr.name == n].values[0][0]:
                print(f'{c.characterName} 픽률: {c.pickRate}%, 승률: {c.winRate}%, 평균 MMR획득: {c.averageMMR}, 모스트 스킨: {c.mostSkin}')
                self.c_name.append(c.characterName)
                self.c_pickRate.append(c.pickRate)
                self.c_winRate.append(c.pickRate)
                self.c_mmr.append(c.averageMMR)
                self.c_skin.append(c.mostSkin)'''

        # 2-2
        # w = input('무기')
        n = self.searchChar
        w = self.searchWeapon
        skinList = pd.DataFrame()

        skinList = pd.concat([skinList, df_characterStats[
            df_characterStats.characterCode == characterNamesKr[characterNamesKr.name == n].code.values[0]]], ignore_index=True)
        gg = f'{n}({w})'
        if n == '알렉스':
            gg = '알렉스'
            img = mpl.image.imread(
                f'{path}/data/mostSkin/45/full.png')
            plt.axis('off')
            plt.imshow(img)
            print('알렉스는 설정상 모든 무기를 다루지만 인게임에서는 밸런스 문제로 권총, 톤파, 암기, 양손검을 사용하는 실험체입니다.')
            print()
            print(f'평균 MMR획득: {mmr:.2f}, 평균 픽률: {pick:.2f}%')
            print(
                f'{df_characterStats[df_characterStats.characterName == gg].characterName.values[0]} 픽률: {df_characterStats[df_characterStats.characterName == gg].pickRate.values[0]}%, 승률: {df_characterStats[df_characterStats.characterName == gg].winRate.values[0]}%, 평균 MMR획득: {df_characterStats[df_characterStats.characterName == gg].averageMMR.values[0]}, 모스트 스킨: {df_characterStats[df_characterStats.characterName == gg].mostSkin.values[0]}')

        elif w in skinList.characterWeapon.values:
            skin = df_characterStats[df_characterStats.characterName == f'{n}({w})'].index[0]
            img = mpl.image.imread(f'{path}/data/mostSkin/{skin}/full.png')
            plt.axis('off')
            plt.imshow(img)
            print(
                f'{df_characterStats[df_characterStats.characterName == gg].characterName.values[0]} 픽률: {df_characterStats[df_characterStats.characterName == gg].pickRate.values[0]}%, 승률: {df_characterStats[df_characterStats.characterName == gg].winRate.values[0]}%, 평균 MMR획득: {df_characterStats[df_characterStats.characterName == gg].averageMMR.values[0]}, 모스트 스킨: {df_characterStats[df_characterStats.characterName == gg].mostSkin.values[0]}')
        else:
            print(f'{n}은 {w}를 사용하지 않는 실험체입니다.')
        self.searchPick = df_characterStats[df_characterStats.characterName == gg].pickRate.values[0]
        self.searchWin = df_characterStats[df_characterStats.characterName == gg].winRate.values[0]
        self.searchMmr = df_characterStats[df_characterStats.characterName == gg].averageMMR.values[0]
        self.searchSkin = df_characterStats[df_characterStats.characterName == gg].mostSkin.values[0]


########################################################################################################################


# 인덱스 페이지
def index():
    print('index() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("ER 웹 크롤링 및 데이터 분석"),
            # pc.box("Progress: editing ", pc.code(filename, font_size="1em")),
            pc.image(src='./thief.png'),
            pc.hstack(
                pc.link(
                    "Squad",
                    href='/squad',
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Character",
                    href='/character',
                    box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                )
            )
        ),
    )


########################################################################################################################


# 스쿼드 사분면 페이지
def squad():
    print('squad() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("Season8 스쿼드(랭크) 사분면"),
            pc.image(src='./squad_default.png'),
            pc.hstack(
                pc.link(
                    "Scatter",
                    href='#',
                    on_click=State.scatter,
                    background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)"
                ),
                pc.link(
                    "Profile",
                    href='#',
                    on_click=State.profile,
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
def character():
    print('character() 실행')
    return pc.center(
        pc.vstack(
            pc.heading("Season8 실험체 검색"),
            pc.image(src='./character_default.png'),
            pc.box("실험체 정보"),
            pc.hstack(
                pc.text("실험체명", font_size="20"),
                pc.input(
                    on_blur=State.set_searchChar,
                    placeholder="Type Character",
                    width="160px"
                )
            ),
            pc.hstack(
                pc.text("사용무기", font_size="20"),
                pc.input(
                    on_blur=State.set_searchWeapon,
                    placeholder="Type Weapon",
                    width="160px"
                )
            ),
            pc.table_container(
                pc.table(
                    pc.thead(
                        pc.tr(
                            # pc.th("무기"),
                            pc.th("픽률(%)"),
                            pc.th("승률(%)"),
                            pc.th("평균 MMR 획득"),
                            pc.th("모스트 스킨")
                        )
                    ),
                    pc.tbody(
                        pc.tr(
                            # pc.td(State.c_name[0]),
                            # pc.td(State.c_pickRate[0]),
                            # pc.td(State.c_winRate[0]),
                            # pc.td(State.c_mmr[0]),
                            # pc.td(State.c_skin[0])
                            pc.td(State.searchPick),
                            pc.td(State.searchWin),
                            pc.td(State.searchMmr),
                            pc.td(State.searchSkin)
                        )
                    ),
                    font_size="20",
                    width="700px"
                )
            ),
            pc.hstack(
                pc.link(
                    "Search",
                    href='#',
                    on_click=State.search,
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


# 홈페이지 적용 및 컴파일
app = pc.App(state=State, style=style)
app.add_page(index, route='/', title='CRUNCH')
app.add_page(squad, route='/squad', title='CRUNCH')
app.add_page(character, route='/character', title='CRUNCH')
app.compile()
