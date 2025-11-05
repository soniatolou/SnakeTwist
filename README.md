# 🐍 Snake Game - Temavärldar

Ett Snake-spel med olika temavärldar inspirerade av populära franchises!

## 🎮 Beskrivning

Detta projekt är skapat för Hackathon TH med temat "Vibe Engineering". Spelet kombinerar klassisk Snake-mekanik med moderna temavärldar där varje värld har sin egen unika visuella stil, färgpalett och känsla.

## 🌍 Tillgängliga Världar

1. **Super Mario World** - It's-a me, Snake-io!
   - Klassiska Mario-färger med blå himmel och röd orm
   - Samla guldmynt!

2. **Hyrule Kingdom (Zelda)** - It's dangerous to go alone!
   - Gröna ängar och Master Sword-blå orm
   - Samla Triforce-guld!

3. **Ohana Island (Stitch)** - Ohana means family!
   - Tropiska färger och Stitch-blå orm
   - Surfa på Hawaii-vibbar!

4. **Kawaii Paradise (Hello Kitty)** - Kawaii desu ne~!
   - Söt rosa värld med Hello Kitty-inspiration
   - Allt är kawaii! 💕

5. **Retro Classic** - Old school vibes!
   - Klassisk svart bakgrund med neon-grön orm
   - Ren nostalgi från 90-talet!

## 🚀 Installation

### Krav
- Python 3.7 eller senare
- Pygame

### Installera Pygame

```bash
pip install pygame
```

Eller använd requirements.txt:

```bash
pip install -r requirements.txt
```

## 🎯 Hur man spelar

### Starta spelet
```bash
python3 snake_game.py
```

### Kontroller

**I menyn:**
- Tryck `1-5` för att välja värld

**Under spelet:**
- `Piltangenter` eller `WASD` - Styr ormen
- `ESC` - Tillbaka till menyn

**Game Over:**
- `SPACE` - Spela igen (samma värld)
- `ESC` - Välj ny värld

## 📋 Spelregler

- Styr ormen för att äta mat (cirklar)
- Ormen växer för varje mat du äter
- Undvik att krocka med väggarna
- Undvik att bita dig själv
- Varje mat ger 10 poäng

## 🎨 Features

- **5 unika temavärldar** med olika färgpaletter
- **Smooth gameplay** med gradient-effekter på ormen
- **Responsiva kontroller** (både piltangenter och WASD)
- **Score tracking** för varje spelomgång
- **Game Over screen** med möjlighet att spela igen eller byta värld
- **Visuella detaljer** - ögon på ormen, rundade hörn, färgade borders

## 🛠️ Teknisk implementation

- **Objektorienterad design** med klasser för Snake, Food, Theme och Game
- **Enum för riktningar** för clean code
- **Arv och polymorfism** för tema-systemet
- **Kollisionsdetektion** för väggar och själv-bitar
- **State management** (menu, playing, game_over)

## 💡 Vidareutveckling (Tips för er!)

Om ni vill utveckla projektet vidare kan ni:
- Lägga till fler temavärldar (Pokemon, Minecraft, Star Wars, etc.)
- Implementera powerups (speed boost, slow down, invincibility)
- Lägga till hinder på banan
- Implementera olika svårighetsgrader
- Lägga till ljud-effekter och musik
- Spara highscores till fil
- Multiplayer-läge
- Animationer mellan övergångar
- Olika mat-typer med olika poäng

## 🎓 Hackathon-värde

**Värde:**
- Roligt spel som är lätt att förstå och spela
- Kan användas för att lära barn programmering
- Visar kreativitet genom temavärldar

**Kreativitet:**
- Unik twist på klassiskt Snake-spel
- Varje värld har sin egen personlighet
- Visuellt tilltalande med färgglada teman

**Teknisk kvalitet:**
- Clean code med tydliga klasser och funktioner
- Lätt att utöka med nya teman
- Bra separation of concerns

## 👥 Credits

Skapat för Hackathon TH - Pythonutveckling
Tema: "Vibe Engineering"

---

Lycka till och ha kul! 🎮✨
