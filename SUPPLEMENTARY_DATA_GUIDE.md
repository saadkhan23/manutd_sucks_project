# Supplementary Data Guide: Recruitment & Investment Analysis

## Overview

To understand **why** Manchester United's performance declined, we need to look beyond on-field statistics to examine the **quality of recruitment decisions** and **resource allocation**. This document outlines valuable data sources and analyses.

---

## 🎯 Core Question: Has Recruitment Played a Role?

**Hypothesis**: Man Utd spent heavily but spent poorly, resulting in:
- Overpaying for declining/unsuited players
- Poor wage structure
- Lack of strategic transfer planning
- Misaligned recruitment with managerial philosophy

---

## 📊 Recommended Supplementary Data Categories

### 1. **Transfer Spending Data** ⭐⭐⭐ (Highest Priority)

#### What to Analyze:
- **Gross spending** (total spent on transfers)
- **Net spending** (total spent - total received)
- **Spending per position** (forwards, midfielders, defenders, GK)
- **Spending per manager** (did each manager get backed?)
- **Number of signings per season**
- **Average fee per signing**

#### Why It Matters:
- Shows if Man Utd are spending but wasting money
- Compares investment levels vs rivals (Man City, Chelsea)
- Reveals if spending correlates with performance (it often doesn't for Man Utd)

#### Key Metrics to Calculate:
```
1. Goals per £100M spent
2. Net spend vs league position correlation
3. Transfer success rate (% of signings who became regulars)
4. Cost per goal/assist (player transfer fee ÷ goal contributions)
```

#### Data Sources:
- **Transfermarkt** (most comprehensive, has API)
- **CIES Football Observatory**
- Kaggle datasets:
  - "EPL Transfer Dataset"
  - "Football Transfer Market Dataset"
- **Football Transfer Tavern** (historical data)

#### Sample Analysis Output:
```
Man Utd Net Spend (2014-2025): £1.2B
Man City Net Spend (2014-2025): £1.4B
Liverpool Net Spend (2014-2025): £450M

Goals per £100M spent:
- Liverpool: 44 goals
- Man City: 38 goals
- Man Utd: 22 goals  ← Inefficiency!
```

---

### 2. **Wage Bill Data** ⭐⭐⭐ (High Priority)

#### What to Analyze:
- **Total wage bill per season**
- **Wages as % of revenue**
- **Wage bill vs league position** (are they overpaying for mediocrity?)
- **Highest earners vs performance** (are star players delivering?)

#### Why It Matters:
- Shows if Man Utd have an unsustainable wage structure
- Reveals if they're paying top-tier wages for mid-tier performance
- Indicates poor contract negotiations (e.g., Sanchez £500k/week)

#### Key Insights to Find:
- Are Man Utd paying top 3 wages but finishing 5th-7th? (inefficiency)
- Wage inflation without performance improvement
- Dead weight contracts (high earners who don't play)

#### Data Sources:
- **Deloitte Football Money League** (annual reports)
- **Capology.com** (player wage estimates)
- **Swiss Ramble** (Twitter/X account with detailed financial analysis)
- Premier League annual financial reports

#### Sample Analysis:
```
2023-24 Season Wage Bills:
1. Man Utd: £215M (6th place finish) ← Inefficient!
2. Man City: £225M (1st place)
3. Chelsea: £195M (12th place) ← Also inefficient
4. Liverpool: £185M (3rd place) ← Efficient

Man Utd: £35.8M per league position
Liverpool: £61.7M per league position
```

---

### 3. **Player Age Profile** ⭐⭐ (Medium-High Priority)

#### What to Analyze:
- **Average squad age per season**
- **Age of new signings** (peak age 24-28 vs declining 29+)
- **Age distribution** (youth vs veterans)
- **Transfer age vs performance**

#### Why It Matters:
- Shows if Man Utd are buying declining players (Casemiro 30, Matic 28, Schweinsteiger 31)
- Indicates lack of strategic planning (buying short-term vs building long-term)
- Reveals if youth development is failing

#### Key Metrics:
- Average age of signings >£30M
- % of squad aged 30+ vs rivals
- Age at purchase vs years of peak performance delivered

#### Data Sources:
- **FBRef** (has age data - already scraped!)
- **Transfermarkt** (age at transfer)
- Player birthdate databases

#### Sample Finding:
```
Average age of £30M+ signings (2014-2024):
- Man Utd: 27.8 years (often past peak)
- Liverpool: 25.2 years (entering peak)
- Man City: 25.8 years (peak years)

Man Utd spent £200M on players aged 29+ (minimal resale value)
```

---

### 4. **Transfer Success Rate** ⭐⭐⭐ (High Priority)

#### What to Analyze:
- **% of signings who became regular starters** (>20 appearances/season)
- **% of signings sold at profit vs loss**
- **Flop rate** (signings sold/loaned out within 2 years)
- **Hit rate by manager** (which manager recruited best?)

#### Why It Matters:
- Directly shows recruitment quality
- Reveals if there's a scouting/decision-making problem
- Compares Man Utd's hit rate to successful clubs

#### Key Questions:
- How many Man Utd signings >£30M flopped? (Maguire, Sancho, Antony, Di Maria)
- What % of signings became club legends vs forgettable?
- Did any manager have a good transfer record?

#### Data Sources:
- **Transfermarkt** (transfer history + appearances)
- **FBRef** (playing time data)
- Manual tracking via Wikipedia/news

#### Sample Analysis:
```
Signings >£50M (2014-2024):

Man Utd Success Rate: 33%
- Success: Bruno Fernandes
- Flop: Maguire, Sancho, Antony, Di Maria, Lukaku, Pogba (debatable)

Man City Success Rate: 75%
- Success: Grealish, Dias, Rodri, De Bruyne, Mahrez, Haaland
- Flop: Phillips, Kalvin (debatable)

Liverpool Success Rate: 85%
- Success: Van Dijk, Alisson, Salah, Núñez (doing well)
- Flop: Keita
```

---

### 5. **Talent Source Analysis** ⭐ (Lower Priority, but interesting)

#### What to Analyze:
- **Countries/leagues where players were signed from**
- **Success rate by source league** (Premier League vs La Liga vs Bundesliga)
- **Nationality diversity**
- **Youth academy contribution vs rivals**

#### Why It Matters:
- Shows if Man Utd are recruiting from the right markets
- Reveals if they're overpaying for Premier League-proven players
- Indicates if youth system is working vs Chelsea/City academies

#### Key Questions:
- Does Man Utd overpay for "Premier League proven" players?
- Are they missing talent from undervalued leagues (Portuguese, Dutch)?
- How does youth academy output compare to rivals?

#### Data Sources:
- **Transfermarkt** (source club/league data)
- **CIES** (nationality reports)
- Academy graduate tracking

#### Interesting Findings to Look For:
```
Man Utd transfer premium for "PL-proven":
- Maguire (Leicester): £80M (overpaid £30M+)
- Wan-Bissaka (Palace): £50M (overpaid £20M+)

Liverpool's bargain hunting:
- Salah (Roma): £36M (underpaid £100M+)
- Robertson (Hull): £8M (underpaid £50M+)

Smart market exploitation:
- Liverpool from Bundesliga: Klopp connections
- Chelsea from France: Ligue 1 talent pipeline
- Man Utd: Scattergun approach, no clear strategy
```

---

### 6. **Manager Backing Analysis** ⭐⭐ (Medium Priority)

#### What to Analyze:
- **Net spend per manager**
- **Number of signings per manager**
- **% of preferred targets actually signed** (did they get their choices?)
- **Time given before sacking** (investment vs patience)

#### Why It Matters:
- Shows if managers were properly backed
- Reveals if Ed Woodward/ownership interfered with recruitment
- Indicates if each manager inherited a mess

#### Key Questions:
- Did Van Gaal, Mourinho, Solskjaer get their first-choice targets?
- How much did each manager spend vs how long they lasted?
- Which manager had best/worst transfer record?

#### Data:
- News reports on "missed targets"
- Transfer window spending per manager
- Manager interview quotes on targets

---

## 🔍 Where to Find This Data

### Free/Accessible Sources:
1. **Transfermarkt.com** ⭐⭐⭐
   - Most comprehensive free database
   - Has API (can scrape legally)
   - Market values, fees, ages, performance
   - https://www.transfermarkt.com/

2. **Kaggle Datasets** ⭐⭐
   - Pre-compiled datasets
   - Search: "Premier League transfers", "football wages"
   - https://www.kaggle.com/datasets

3. **Capology.com** ⭐⭐
   - Player wage estimates
   - Squad salary breakdowns
   - https://www.capology.com/

4. **Deloitte Football Money League** ⭐
   - Annual reports (free PDFs)
   - Wage bills, revenues
   - https://www2.deloitte.com/uk/en/pages/sports-business-group/articles/deloitte-football-money-league.html

5. **Swiss Ramble** (Twitter/X) ⭐⭐
   - Fantastic financial analysis threads
   - Charts on spending, wages, efficiency
   - https://twitter.com/SwissRamble

### Paid/Premium Sources:
1. **CIES Football Observatory**
   - Academic-grade data
   - Player valuations, transfer analysis

2. **Opta/StatsBomb**
   - Advanced player performance data
   - Can link spending to xG contributions

3. **Transfermarkt API (unofficial)**
   - Can be scraped programmatically

---

## 📈 Proposed Analyses (Prioritized)

### Phase 1: Quick Wins (1-2 hours)
1. ✅ **Find Kaggle transfer dataset** for Premier League
2. ✅ **Scrape Transfermarkt** for Man Utd + rivals spending (2014-2025)
3. ✅ **Calculate**: Net spend, gross spend, signings per season
4. ✅ **Visualize**: Man Utd spending vs rivals vs league position

### Phase 2: Deep Dive (3-5 hours)
5. **Transfer success rate**: Manually classify signings as hit/flop/ok
6. **Cost per goal contribution**: Transfer fee ÷ career goals+assists
7. **Age analysis**: Average age of signings, % bought in prime vs decline
8. **Manager backing**: Net spend per manager, correlation with results

### Phase 3: Advanced (5+ hours)
9. **Wage efficiency**: Wage bill vs points, compare to rivals
10. **Talent source map**: Where did successful vs failed signings come from?
11. **Youth academy output**: Academy grads in first team vs rivals
12. **Predictive modeling**: Can we predict Man Utd's future based on current recruitment?

---

## 🎯 Expected Insights from Recruitment Analysis

Based on public knowledge, we expect to find:

### Man Utd Transfer Failures:
1. **Overpaying for declining players** (Casemiro 30, Varane 28)
2. **Panic buying** (deadline day signings, overpaying for "PL-proven")
3. **Poor resale value** (buying high, selling low or free releases)
4. **Manager mismatch** (signing players for previous manager's system)
5. **Ignoring analytics** (eye test signings vs data-driven rivals)

### Rival Success Patterns:
1. **Man City**: Bought younger, strategic, systematic (Pep's philosophy)
2. **Liverpool**: Data-driven scouting, undervalued markets, high hit rate
3. **Arsenal**: Youth + strategic experience, wage discipline
4. **Leicester (2016)**: Moneyball approach, undervalued gems

### The Recruitment Story:
- Man Utd spent **similar amounts** to rivals
- But got **23% fewer goals per game**
- Because they made **poor recruitment decisions**
- Driven by **managerial instability** and **lack of strategy**

---

## 🚀 Next Steps: How to Proceed

### Option 1: Quick Transfer Spending Analysis (Recommended)
1. Find Kaggle Premier League transfer dataset
2. Load and clean data
3. Calculate net spend for top 7 teams (2014-2025)
4. Correlate spending with goals/game and league position
5. Create visualizations showing Man Utd's spending inefficiency

**Time**: ~2 hours
**Impact**: High - directly answers "Did they spend poorly?"

### Option 2: Scrape Transfermarkt
1. Use Transfermarkt scraper library (or build one)
2. Pull transfer data for Man Utd + rivals
3. Enrich with player age, position, fee
4. Analyze as above

**Time**: ~3-4 hours
**Impact**: High - more complete dataset

### Option 3: Manual Research + Existing Data
1. Use Wikipedia/news for major transfers (>£30M)
2. Classify 30-40 major signings as hit/flop
3. Calculate success rate vs rivals
4. Combine with existing FBRef performance data

**Time**: ~1-2 hours
**Impact**: Medium-high - smaller sample but still valuable

---

## 💬 Recommendation

**Start with transfer spending** (Option 1 or 2). This will:
- ✅ Directly answer: "Has recruitment been the problem?"
- ✅ Show if Man Utd spent as much as rivals but got less output
- ✅ Create powerful visualizations (spending vs goals/game)
- ✅ Support narrative: "They spent £1B+ and got worse"

**Then add wage data** from Deloitte/Capology if available.

**Save age/talent source analysis** for bonus content if time allows.

---

## 🔗 Quick Resource Links

- **Kaggle Transfer Data**: https://www.kaggle.com/search?q=premier+league+transfers
- **Transfermarkt**: https://www.transfermarkt.com/manchester-united/transfers/verein/985
- **Capology Wages**: https://www.capology.com/club/manchester-united/salaries/
- **Swiss Ramble Man Utd Analysis**: https://twitter.com/SwissRamble (search "Manchester United")
- **Deloitte Reports**: https://www2.deloitte.com/uk/en/pages/sports-business-group/articles/deloitte-football-money-league.html

---

**Let me know which direction you'd like to go, and I'll start pulling in the data!** 🚀
