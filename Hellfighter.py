import random
import time
import sys
import os

# 初始化回合计数
roundcount = 1
#初始化强化次数
strengthencount = 0
#初始化闪避次数
misscount = 0
# 构造玩家
class Player(object):

    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attackpoint = 15  # 自身攻击力
        self.defensepoint = 10  # 自身防御力
        self.weapon = Weapon('Wooden Sword', 10)  # 初始武器及伤害
        self.armor = Armor('Wooden Armor', 5)  # 初始防具及防御力
        self.magic = 100  # 初始蓝量
    
    # 玩家攻击
    def attack(self, enemy):
        total_attackpoint = self.attackpoint + self.weapon.attack_bonus  # 总伤害
        enemy.take_damage(total_attackpoint)
    
    # 玩家技能
    def skills(self, enemy, player):

        if self.magic < 10:
            print_action(f"{self.name} 魔法不足！\n")
            return
        
        else:
            self.magic -= 10
            print_action('蓝量减少 10 ！\n')
        
        skillnum = random.randint(1, 100)

        if skillnum <= 20:#暴击技能
            self.attackpoint *= 1.4
            total_attackpoint = int(self.attackpoint + self.weapon.attack_bonus)  # 总伤害
            enemy.take_damage(total_attackpoint)
            print_action(f"{self.name} 使用技能---暴击！对 {enemy.name} 造成 {int(total_attackpoint)} 伤害！\n")
            self.attackpoint /= 1.4
           
            
        elif skillnum >20 and skillnum <= 40:#永久加防御
            self.defensepoint *= 1.2
            self.defensepoint = int(self.defensepoint)
            print_action(f"{self.name} 使用技能---强化！自身防御力提升至 {int(self.defensepoint + self.armor.defense_bonus)}！\n")
           
        
        elif skillnum > 40 and skillnum <= 60:#削弱敌人
            enemy.enemy_attack *= 0.9
            enemy.enemy_attack = int(enemy.enemy_attack)
            print_action(f"{self.name} 使用技能---削弱！敌人攻击力降低至 {int(enemy.enemy_attack)}！\n")
            
        elif skillnum >60 and skillnum <= 80:#永久加攻击
            self.attackpoint *= 1.2
            self.attackpoint = int(self.attackpoint)
            print_action(f"{self.name} 使用技能---攻击强化！自身攻击力提升至 {int(self.attackpoint + self.weapon.attack_bonus)}！\n")
        
        elif skillnum == 97 or skillnum == 98:
            enemy.take_damage(99999)
            print_action(f"{self.name} 一击必杀！\n")

        else:
            print_action(f"{self.name} 使用技能---没放出来！\n")
            pass

    
    # 玩家回血
    def heal(self):
        health_to_restore = int(self.health * 0.2)  # 回当前血量的20%
        self.health += health_to_restore
        print_action(f'{self.name} 回复了 {int(health_to_restore)} 生命。\n')
      
    # 玩家闪避  
    def miss(self, enemy):
        global misscount
        misscount += 1
        print_action(f"{self.name} 第 {misscount} 次闪避！\n")
        if misscount > 15:
            print_action(f"{self.name} 闪避次数已用完！\n")
            return "n"
        
        else:
            num = random.randint(1, 100)
            if num >= 80:  # 20%触发
                print_action(f"{self.name} 闪避了攻击，并重击了敌人，造成{int(enemy.health * 0.4)} 伤害！\n")
                return "y1"
            elif num > 20 and num < 80: #60%触发
                print_action(f"{self.name} 闪避了攻击！\n")
                return "y2"
            else:
                print_action(f"{self.name} 未能闪避攻击，受到 {int(self.health * 0.4)} 重击！\n")
                return "n"

        
    
    
    # 玩家受伤
    def take_damage(self, damage):  
        actual_damage = max(damage - (self.defensepoint + self.armor.defense_bonus), 0)  # 实际受到的伤害
        self.health -= actual_damage
       
    # 玩家装备武器 
    def equip_weapon(self, weapon):
        self.weapon = weapon
        print_action(f'{self.name} 已装备 {weapon.name}。攻击力提升至 {int(self.attackpoint + self.weapon.attack_bonus)}！\n')
    
    # 玩家装备护甲
    def equip_armor(self, armor):
        self.armor = armor
        print_action(f'{self.name} 已装备 {armor.name}。 防御力提升至 {int(self.defensepoint + self.armor.defense_bonus)}！\n')

# 构造武器
class Weapon(object):
    def __init__(self, name, attack_bonus):
        self.name = name
        self.attack_bonus = attack_bonus  # 武器攻击力
 
# 构造护甲       
class Armor(object):
    def __init__(self, name, defense_bonus):
        self.name = name
        self.defense_bonus = defense_bonus  # 护甲防御力

# 构造敌人
class Enemy(object):
    def __init__(self, name, enemy_attack, health):
        self.name = name
        self.enemy_attack = enemy_attack  # 敌人攻击和血量
        self.health = health
    
    # 思路：每轮让敌人随机选择行动（攻击或回血）
    def enemyaction(self, player):
        actnum = random.randint(1, 100)
        
        if actnum <= 70:
            self.enemyattack(player)
            print_action(f"{self.name} 攻击了 {player.name}！\n")
            
        elif actnum > 60 and self.health < int(self.health * 0.6):
            self.enemyheal()
            print_action(f"{self.name} 治疗自己！\n")
            
        elif actnum >= 85:
            
            if random.randint(1, 100) >= 50:
                self.enemydebuff(player)
                print_action(f"{self.name} 试图加入 {player.name} 的后宫，使之心烦意乱！\n")
                print_action(f"{player.name} 的生命减少了！\n{player.name} 的攻击减少了！\n{player.name} 的防御减少了！\n")
            else:
                print_action(f"{self.name} 妄图诱惑 {player.name}，可是没有卵用！\n")
        
        else:
            self.enemystrengthen()

    def take_damage(self, damage):
        self.health -= damage
    
    # 敌人攻击
    def enemyattack(self, player):
        player.take_damage(self.enemy_attack)  # 玩家受伤
    
    # 敌人回血
    def enemyheal(self):
        healthpoint = int(self.health * 0.3)
        self.health += healthpoint
    
    #敌人削弱玩家
    def enemydebuff(self, player):
        player.health = int(player.health * 0.9)
        player.defensepoint = int(player.defensepoint * 0.9)
        player.attackpoint = int(player.attackpoint * 0.9)
        player.magic = int(player.magic * 0.9)
        
    #敌人强化    
    def enemystrengthen(self):
        global strengthencount
        strengthencount += 1
        enemy_attack_bonus = int(self.enemy_attack * 0.1)
        if strengthencount <= 10:
            self.enemy_attack += enemy_attack_bonus
            print_action(f"{self.name} 强化了！攻击力提升至 {int(self.enemy_attack)}！\n")
        else:
            print_action(f"{self.name} 强化次数已用完！\n")
    

# 按等级生成敌人，第一轮为level为1，以此类推，打败一轮之后level加1，就能生成level为2的敌人
def generate_enemy(level):
    enemies = {
        0: ("「博学宗师」制造的 原型人偶", 15, 100),
        1: ("「疲惫之恶魔」潘德莫妮卡", 20, 100),
        2: ("「色欲之恶魔」莫德乌斯", 40, 125),
        3: ("「地狱三头犬」刻俄柏洛斯", 55, 175),
        4: ("「抱怨之恶魔」玛琳娜", 65, 225),
        5: ("「放荡之恶魔」兹达拉", 80, 250),
        6: ("「好奇天使」阿撒兹勒", 90, 275),
        7: ("“正义”", 100, 300),
        8: ("「地狱CEO」路西法", 120, 350),
        9: ("“大检察官”", 145, 400)
    }
    
    if level in enemies:
        name, attack, health = enemies[level]
        return Enemy(name, attack, health)
    else:
        raise ValueError(f"Invalid level: {level}. Level must be between 1 and 9.")


# 生成武器，level1打败自动掉落level1对应的武器并自动装备
def generate_weapon(level):
    weapons = {
        0: ("起始武器", 0),
        1: ("石剑", 15),
        2: ("铁剑", 25),
        3: ("钻石剑", 35),
        4: ("御剑", 40),
        5: ("裁决", 50),
        6: ("武藏", 60),
        7: ("伊川", 70),
        8: ("洛阳", 80),
        9: ("石中剑", 100)
    }
    
    if level in weapons:
        return Weapon(*weapons[level])
    else:
        raise ValueError(f"Invalid level: {level}. Level must be between 1 and 9.")

        

# 生成护甲，和武器差不多
def generate_armor(level):
    armors = {
        0: ("起始装备", 0),
        1: ("石甲", 15),
        2: ("铁甲", 30),
        3: ("钻石甲", 40),
        4: ("成步堂", 50),
        5: ("艾森豪威尔", 60),
        6: ("平乐", 70),
        7: ("世田谷", 75),
        8: ("鬼塚", 85),
        9: ("神绮", 95)
    }
    
    if level in armors:
        return Armor(*armors[level])
    else:
        raise ValueError(f"Invalid level: {level}. Level must be between 1 and 9.")

# 转换数据类型
def to_int(player):
    player.health = int(player.health)
    player.attackpoint = int(player.attackpoint)
    player.defensepoint = int(player.defensepoint)
    player.magic = int(player.magic)

# 滚动文字输出逻辑
def print_action(message):
    for text in message:
        print("\033[1;31m" + text + "\033[0m", end = "", flush = True)
        time.sleep(0.03)

def print_context(message):
    for text in message:
        print(text, end = "", flush = True)
        time.sleep(0.03)

def print_conversation(name, message):
    for text in name:
        print("\033[1;31m" + text + "\033[0m", end = "", flush = True)
        time.sleep(0.03)
    for text in message:
        print(text, end = "", flush = True)
        time.sleep(0.1)

def print_story(message):
    for text in message:
        print("\033[1;33m" + text + "\033[0m", end = "", flush = True)
        time.sleep(0.05)
        

# 死亡场景
def game_over(player):
    list = ["伴随死亡而来的，比死亡本身更可怕。", "猝然死去本无甚苦痛，长期累死倒真难以忍受。", "怕死比死更可怕。", "寒冷寂寞的生，却不如轰轰烈烈的死。", "死并非生的对立面，而作为生的一部分永存。", "生荣死哀,身没名显。"]
    print_action(f"{player.name} 已被击败。\n {'-' * 15} 游  戏  结  束 {'-' * 15}\n")
    num = random.randint(1, 6)
    time.sleep(1.0)
    print_conversation("别西卜：", f"{list[num - 1]}\n")
    time.sleep(1.0)
    print_context("1.别西卜，我不服。（前往来生） | 2.你可知道现在的我亦是过去的我。（读取存档） | 3.就这样吧。（退出游戏）| 4.这些句子都是你说的么？\n")
    choice = input(">>>")
    if choice == "1":
        print_conversation("别西卜：", "陷入冲动会使你无法自拔。\n")
        time.sleep(1.0)
        new_game()
    elif choice == "2":
        print_conversation("别西卜：", "我很想知道你什么时候能战胜过去的自己。\n")
        time.sleep(1.0)
        load_game()
    elif choice == "3":
        print_conversation("别西卜：", "你想要建议，但无人可问。\n")
        time.sleep(1.0)
        sys.exit()
    else:
        print_conversation("别西卜：", "当然不是。\n")
        time.sleep(1.0)
        game_over(player)

# 通关场景
def game_victory(player):
    print_action(f"{player.name} 已通关！\n")
    time.sleep(1.0)
    print_conversation("别西卜：", "这就是Hellfighter的故事\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "由善良的老别西卜为您讲述。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "我知道我知道，这本该由你自己来讲述。但我就是情不自禁。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "我猜你会疑问。这真的发生过吗？Hellfighter在哪里？\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "也许你就是那个Hellfighter？只不过在这深渊待太久你忘了而已。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "或许你根本不存在？而只是我这只可怜的老苍蝇自言自语罢了。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "嚯嚯，为了这个故事，有些问题还是留着别问吧。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "直到下次。\n")
    time.sleep(1.0)
    print_action("1.再来！| 2.再见。\n")
    choice = input(">>>")
    if choice == "1":
        print_conversation("别西卜：", "下次回来，不要忘了带巧克力卷饼。\n")
        time.sleep(1.0)
        new_game()
    else:
        print_conversation("别西卜：", "再见。\n")
        time.sleep(1.0)
        sys.exit()

#进度条
def bar():
    width = 50
    
    for i in range(101):
        filled = int((width * i)/100)
        empty = width - filled
        
        loading = '=' * filled + '-' * empty
        print(f"\rLoading {i}%[{loading}]", end="", flush=True)
    
        time.sleep(0.03)

# 载入存档
def load_game():
    global roundcount, strengthencount, misscount
    save_path = os.path.join(full_path, 'save.htsave')
    root, ext = os.path.splitext(save_path)
    original_name = root + ".txt"
    os.rename(save_path, original_name)
    save_path = original_name
    f_name = open(save_path, 'r')
    data = f_name.readlines()
    f_name.close()
    
    if len(data) == 1:
        print_action("未找到存档，将为您创建一个新游戏。\n")
        time.sleep(1.0)
        root1, ext1 = os.path.splitext(save_path)
        new_name = root + ".htsave"
        os.rename(save_path, new_name)
        time.sleep(1.0)
        new_game()
        return
    else:
        pass
    player_name = data[0].strip()
    player_health = int(data[1].strip())
    player_attackpoint = int(data[2].strip())
    player_defensepoint = int(data[3].strip())
    player_magic = int(data[4].strip())
    save_level = int(data[5].strip())
    player = Player(player_name)
    player.health = player_health
    player.attackpoint = player_attackpoint
    player.defensepoint = player_defensepoint
    player.magic = player_magic
    level = save_level
    enemy_name = data[6].strip()
    enemy_attack = int(data[7].strip())
    enemy_health = int(data[8].strip())
    roundcount = int(data[9].strip())
    strengthencount = int(data[10].strip())
    misscount = int(data[11].strip())
    enemy = Enemy(enemy_name, enemy_attack, enemy_health)
    print_action(f"已载入存档：{player_name}，生命值：{int(player_health)}，攻击力：{int(player_attackpoint)}，防御力：{int(player_defensepoint)}，蓝量：{int(player_magic)}，当前层数：{level}\n")
    root1, ext1 = os.path.splitext(save_path)
    new_name = root + ".htsave"
    os.rename(save_path, new_name)

    if level > 1:
        player.equip_weapon(generate_weapon(level-1))
        player.equip_armor(generate_armor(level-1))
    else:
        print_action("身上无装备！\n")
    play(player, level, enemy)

# 保存存档
def save_game(player, level, enemy):
    save_path = os.path.join(full_path, 'save.htsave')
    root1, ext1 = os.path.splitext(save_path)
    original_name = root1 + ".txt"
    os.rename(save_path, original_name)
    save_path = original_name
    f_name = open(save_path, 'w')
    data = [player.name + '\n', str(player.health) + '\n', str(player.attackpoint) + '\n', str(player.defensepoint) + '\n', str(player.magic) + '\n', str(level) + '\n', str(enemy.name) + '\n', str(enemy.enemy_attack) + '\n', str(enemy.health) + '\n', str(roundcount) + '\n', str(strengthencount) + '\n', str(misscount) + '\n']
    f_name.writelines(data)
    f_name.close()
    print_action(f"已保存存档：{player.name}，生命值：{int(player.health)}，攻击力：{int(player.attackpoint)}，防御力：{int(player.defensepoint)}，蓝量：{int(player.magic)}，当前层数：{level}\n")
    root, ext = os.path.splitext(save_path)
    new_name = root + ".htsave"
    os.rename(save_path, new_name)

# 教程
def tutorial(player_name):
    print_action(f"{player_name}，欢迎来到 Hellfighter©️ 教程！\n")
    time.sleep(1.0)
    print_conversation("别西卜：", f"{player_name}，早安。\n")
    time.sleep(0.5)
    print_story("此处省略剧情部分。游戏剧情尚未完善，敬请期待。\n")
    time.sleep(1.0)
    print_conversation("别西卜：", "首先我们了解攻击。所谓「工欲善其事必先利其器」，武器可以给你的攻击提供相当一部分加成。这也就是说你对恶魔们造成的攻击等于「自身攻击力」与「武器攻击力」的「总和」。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "想必无需多言吧。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "接着，请你感受你身体内的「魔力」。用它可以施展法术，要么能迷惑你的对手，要么能让自己更强大，要么，什么也不会发生————或许勤加练习可以让法术更稳定呢。（请期待后续更新的Rougelike和RPG元素）\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "这是Loremaster（智识之恶魔）要给你的神奇补剂。不过你得慎用，毕竟不知道她到底掺了什么东西进去。血量低于75再用吧，免得上瘾之类的。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "「闪避」————我想你还是普通人的时候就会这一招————这叫做以退为进。运气好，说不定可以抓住破绽一击制敌。运气不好则有可能被倒打一耙。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "目前我能想到的就这么多。\n")
    time.sleep(2)
    print_conversation("别西卜：", "Loremaster刚刚拿了个小木偶过来说要给你练练。\n")
    time.sleep(0.5)
    print_conversation("别西卜：", "那么，在实战中检验吧。\n")
    time.sleep(0.3)
    print_conversation("「博学宗师」：", "哈咯哈咯，好久不见呀~\n")
    time.sleep(0.3)
    print_conversation("别西卜：", "他好像不是那位。\n")
    time.sleep(0.3)
    print_conversation("「博学宗师」：", "哦，认错了么，还真像呢......\n")
    time.sleep(0.3)
    print_conversation("「博学宗师」：", "你，听好咯，我这人偶设计的时候模仿地狱的恶魔们，可攻可守，还会花招，造起来可麻烦了！你要是劲大就轻点下手，别三两下给整坏了。要是人不行的话嘛~我这小玩意也不会伤到你什么的啦，放心放心~\n")
    time.sleep(1)
    print_conversation("「博学宗师」：", "罢了，总之先拿这人偶验验你的实力！\n")
    time.sleep(1)
    tu_fight(player_name)
    time.sleep(0.5)
    print_conversation("别西卜：", "到此为止。\n")
    time.sleep(1)
    print_action("要重新开始新手教程吗？\n")
    time.sleep(0.5)
    print_action("1.是 | 2.否\n")
    choice = int(input(">>> "))
    if choice == 1:
        tutorial(player_name)
    else:
        print_conversation("「博学宗师」：", "雷厉风行呀，还真像呢......\n")

#教程战斗
def tu_fight(player_name):
    global roundcount, strengthencount, misscount
    enemy = generate_enemy(0)
    player = Player(player_name)
    player.armor = Armor("起始装备", 0)
    player.weapon = Weapon("起始武器", 0)
    while True:  # 构造无限循环
        print_action(f"{enemy.name} 出现了！\n")
        time.sleep(1.0)
        
        while enemy.health > 0:
            global roundcount
            print("\n" + "=" * 50)  # 美化勿动
            print_action(f"{player.name} 对阵 {enemy.name} 的第 {roundcount} 回合！\n")
            
            time.sleep(0.2)
            print(f"玩家：{player.name} | 生命：{int(player.health)} | 攻击：{int(player.attackpoint + player.weapon.attack_bonus)} | 防御：{int(player.defensepoint + player.armor.defense_bonus)}| 蓝量：{int(player.magic)}")
            print(f"敌人：{enemy.name} | 生命：{int(enemy.health)} | 攻击：{int(enemy.enemy_attack)}")
            print("1.攻击 | 2.技能 | 3.治疗 | 4.闪避\n")
            time.sleep(0.2)
            choice = input("本轮行动是：")
            
            
            if choice == '1':
                player.attack(enemy)  # 玩家攻击
                print_action(f"{player.name} 已攻击 {enemy.name}！造成了 {int(player.attackpoint + player.weapon.attack_bonus)} 点伤害！\n")

                if player.health <= 0:  # 玩家死亡
                    print_conversation("「博学宗师」：", "骗人的吧，重来！\n")
                    tu_fight(player_name)
                
                if enemy.health <= 0:  # 敌人死亡掉装备
                    print_action(f"{player.name} 击败了 {enemy.name}！\n")
                    print_conversation("「博学宗师」：", "很好！我从你身上看到了一位故人的影子！\n")
                    time.sleep(0.4)
                    print_conversation("「博学宗师」：", "或许我没有看错呢......\n")
                    time.sleep(1)
                    roundcount = 1
                    misscount = 0
                    strengthencount = 0
                    return

                
                enemy.enemyaction(player)  # 让敌人随机行动
                time.sleep(0.5)  # 延迟0.5s
            
            elif choice == '2':
                player.skills(enemy, player)
                enemy.enemyaction(player)

                if enemy.health <= 0:  # 敌人死亡
                    print_action(f"{player.name} 击败了 {enemy.name}！\n")
                    print_conversation("「博学宗师」：", "很好！我从你身上看到了一位故人的影子！\n")
                    time.sleep(0.4)
                    print_conversation("「博学宗师」：", "或许我没有看错呢......\n")
                    time.sleep(1)
                    roundcount = 1
                    misscount = 0
                    strengthencount = 0
                    return

            
            elif choice == '3' and player.health <= 75:
                player.heal()
                enemy.enemyaction(player)
                time.sleep(0.5)
            
            elif choice == '4':
                result = player.miss(enemy)
                if result == "n":
                    enemy.enemyaction(player)
                    player.health = int(max(player.health * 0.6, 0))
                    time.sleep(0.5)
                elif result == "y1":
                    enemy.take_damage(int(enemy.health * 0.4))
                    time.sleep(0.5)
                else:
                    time.sleep(0.5)
            
            else:
                time.sleep(0.5)
                print_action("键入命令无效或者生命值大于75！\n")

            roundcount += 1
             
            if player.health <= 0:  # 玩家死亡
                print_conversation("「博学宗师」：", "骗人的吧，重来！\n")
                tu_fight(player_name)

            to_int(player)  # 转换数据类型
    
        

# 新游戏
def new_game():
    print_action("！！注意！！\n")
    time.sleep(0.2)
    print_action("本游戏没有自动存档功能，请注意手动存档。\n")
    time.sleep(0.2)
    print_action("当前版本只有一个存档位，请合理安排。\n\n")
    time.sleep(0.5)
    print_story("这个故事发生在一位勇者身上，他的名字是：")
    player_name = input()
    print_action(f"\n{player_name}，你好！\n")
    time.sleep(0.5)
    print_action("要开始新手教程吗？\n")
    time.sleep(0.5)
    print_action("1.是 | 2.否\n")
    choice = int(input(">>> "))

    if choice == 1:
        tutorial(player_name)
    else:
        pass

    print_action(f"{player_name}，踏上了征途。\n")
    time.sleep(0.5)
    player = Player(player_name)  # 实例化玩家

    #后门
    if player_name == "刘金奕":
        print_action("已进入测试模式。已进入测试模式。已进入测试模式。\n")
        player.health = 9999
        player.attackpoint = 9999
        player.magic = 9999
        player.defensepoint = 9999
    else:
        pass
    
    level = 1  # 初始化level
    enemy = generate_enemy(level)  # 生成level1敌人
    play(player, level, enemy)

# 开始界面
def start():
    print_context("您正在游玩 Hellfighter©️ ver2.3.1_20250112-Beta\n作者：Samustach\n")
    time.sleep(0.5)
    bar()
    time.sleep(0.5)
    print("\n")
    print_action("1.新游戏 | 2.载入存档 | 3.退出游戏\n")
    choice = int(input(">>> "))

    if choice == 1:
        new_game()
    elif choice == 2:
        load_game()
    else:
        print_action("C U Next Time!\n")
        time.sleep(1)
        sys.exit()


# 主程序
def play(player, level, enemy):
    global roundcount, strengthencount, misscount
    while True:  # 构造无限循环
        print_action(f"{enemy.name} 出现了！\n")
        time.sleep(1.0)
        
        while enemy.health > 0:
            global roundcount
            print("\n" + "=" * 50)  # 美化勿动
            print_action(f"{player.name} 对阵 {enemy.name} 的第 {roundcount} 回合！\n")
            
            time.sleep(0.2)
            print(f"玩家：{player.name} | 生命：{int(player.health)} | 攻击：{int(player.attackpoint + player.weapon.attack_bonus)} | 防御：{int(player.defensepoint + player.armor.defense_bonus)}| 蓝量：{int(player.magic)}")
            print(f"敌人：{enemy.name} | 生命：{int(enemy.health)} | 攻击：{int(enemy.enemy_attack)}")
            print("1.攻击 | 2.技能 | 3.治疗 | 4.闪避 | 5.保存并退出\n")
            time.sleep(0.2)
            choice = input("本轮行动是：")
            
            
            if choice == '1':
                player.attack(enemy)  # 玩家攻击
                print_action(f"{player.name} 已攻击 {enemy.name}！造成了 {int(player.attackpoint + player.weapon.attack_bonus)} 点伤害！\n")

                if player.health <= 0:  # 玩家死亡
                    game_over(player)
                    return
                
                if enemy.health <= 0:  # 敌人死亡掉装备
                    player.equip_weapon(generate_weapon(level))
                    player.equip_armor(generate_armor(level))
                    print_action(f"{player.name} 击败了 {enemy.name}！\n")
                    time.sleep(0.4)
                    
                    break  # 跳出while enemy.health > 0循环，到level += 1那行，此时还在while True循环里
                
                enemy.enemyaction(player)  # 让敌人随机行动
                time.sleep(0.5)  # 延迟0.5s
            
            elif choice == '2':
                player.skills(enemy, player)
                enemy.enemyaction(player)

                if enemy.health <= 0:  # 敌人死亡掉装备
                    player.equip_weapon(generate_weapon(level))
                    player.equip_armor(generate_armor(level))
                    print_action(f"{player.name} 击败了 {enemy.name}！\n")
                    
                    break  # 跳出while enemy.health > 0循环，到level += 1那行，此时还在while True循环里
                time.sleep(0.5)
            
            elif choice == '3' and player.health <= 75:
                player.heal()
                enemy.enemyaction(player)
                time.sleep(0.5)
            
            elif choice == '4':
                result = player.miss(enemy)
                if result == "n":
                    enemy.enemyaction(player)
                    player.health = int(max(player.health * 0.6, 0))
                    time.sleep(0.5)
                elif result == "y1":
                    enemy.take_damage(int(enemy.health * 0.4))
                    time.sleep(0.5)
                else:
                    time.sleep(0.5)
                    # 概率中了就跳过敌人攻击阶段

            elif choice == '5':
                save_game(player, level, enemy)
                time.sleep(0.5)
                print_conversation("别西卜：", "临阵脱逃。\n")
                time.sleep(1.0)
                sys.exit()  # 保存退出游戏
            
            elif choice == '/kill @s':
                game_over(player)

            else:
                time.sleep(0.5)
                print_action("键入命令无效或者生命值大于75！\n")

            roundcount += 1
             
            if player.health <= 0:  # 玩家死亡
                game_over(player)
                sys.exit()  # 死亡退出游戏

            to_int(player)  # 转换数据类型

        level += 1  # 本行只有在某一level敌人死后才运行
        strengthencount = 0#重置强化次数
        roundcount = 1#重置回合
        player.magic = int(100 - ((level - 1) * 10))#蓝量恢复
        misscount = 0#重置闪避次数
        
        if level > 9:  
            game_victory(player)
            sys.exit()  # 通关退出游戏

        enemy = generate_enemy(level)  # 生成下一层敌人

docu_path = os.path.expanduser("~/Documents")
folder_name = 'Hellfighter'
file = 'save.htsave'
full_path = os.path.join(docu_path, folder_name)
if not os.path.exists(full_path):
    os.makedirs(full_path)
    # 保存游戏数据
    f_name = open(os.path.join(full_path, 'save.txt'), 'w')
    initial_data = ['0']
    f_name.writelines(initial_data)
    f_name.close()
    save_path = os.path.join(full_path, 'save.txt')
    root, ext = os.path.splitext(save_path)
    new_name = root + ".htsave"
    os.rename(save_path, new_name)
else:
    try:
        open(os.path.join(full_path, file), 'r')
    except FileNotFoundError:
        f_name = open(os.path.join(full_path, 'save.txt'), 'w')
        initial_data = ['0']
        f_name.writelines(initial_data)
        f_name.close()
        save_path = os.path.join(full_path, 'save.txt')
        root, ext = os.path.splitext(save_path)
        new_name = root + ".htsave"
        os.rename(save_path, new_name)
    else:
        pass

start()