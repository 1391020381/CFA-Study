# Session Notes - October 25, 2025

## Session Overview
- **Date**: 2025-10-25
- **Duration**: ~60 minutes
- **Format**: Mixed - Practice problem testing + Concept deep dives
- **Main Topics**: Bond yield rankings (verification), Multi-stage dividend discount model, Investment risk types, Options vs Futures
- **Days Until Exam**: 16 days

---

## Practice Problems and Concept Reviews

### Topic 1: Bond Yield Rankings - Practice Verification (D.32)

**Topic**: D.32 Bond and stock valuation - Yield rankings reinforcement

**Purpose**: Test student's retention of yesterday's learning (bond yield rankings)

**Problem Given**: Corporate bond issued 5 years ago, 6% annual coupon, 20-year maturity (15 years remaining), $1,000 par, trading at $920, callable in 3 years at $1,040.

**Question**: Rank yields from LOWEST to HIGHEST: CR, CY, YTM, YTC

**Options**:
- A) CR < CY < YTM < YTC ✓
- B) YTC < YTM < CY < CR
- C) CR < CY < YTC < YTM
- D) CY < CR < YTM < YTC

**Student's Response**: "CR < CY < YTM < YTC" ✓ **CORRECT**

---

**Student's Work Shown**:

**Coupon Rate**: 6% ✓ (correctly identified as fixed)

**Current Yield**:
- Calculation: $60 ÷ $920 = 0.0652 = **6.52%** ✓
- Perfect calculation!

**Bond Status**: Identified as **DISCOUNT bond** ✓
- Price $920 < Par $1,000

**Ranking Applied**: **CR < CY < YTM < YTC** ✓
- Correctly applied discount bond pattern from yesterday's learning!

---

**YTC Calculation Attempt**:

Student attempted: "40/8+60=65, 0.65"
- Trying to approximate YTC
- Got confused on exact method

**Teaching Moment - YTC Approximation Formula**:

After student challenged my initial numbers (correctly!), I searched for proper formula:

**Approximate YTC Formula**:
```
YTC = [Annual Coupon + (Call Price - Current Price) ÷ Years to Call] ÷ [(Call Price + Current Price) ÷ 2]
```

**Applied to our bond**:
- YTC = [$60 + ($1,040 - $920) ÷ 3] ÷ [($1,040 + $920) ÷ 2]
- YTC = [$60 + $40] ÷ $980
- YTC = $100 ÷ $980
- **YTC = 10.2%** ✓

**YTM Approximation**:
- YTM ≈ [$60 + ($1,000 - $920) ÷ 15] ÷ [($1,000 + $920) ÷ 2]
- YTM ≈ [$60 + $5.33] ÷ $960
- **YTM ≈ 6.8%**

**Final Verified Ranking**:
- CR = 6.0% (lowest)
- CY = 6.52%
- YTM = 6.8%
- YTC = 10.2% (highest)

**CR < CY < YTM < YTC** ✓ Student was 100% correct!

---

**Important Teaching Moment - Timeline Clarification**:

**Student's Question**: "Why 3 years for YTC, not 5+3 years?"

**Confusion**: Student thought "issued 5 years ago" + "callable in 3 years" = 8 years

**Clarification Provided**:

**Timeline Visual**:
```
5 years ago              TODAY                3 years           15 years
    |                      |                     |                  |
  Issued              You buy bond          Callable          Maturity
  (20-yr)              at $920              at $1,040         at $1,000
    |                      |                     |                  |
    └──────5 years────────┘                     └────15 years──────┘
    (already passed)                         (remaining to maturity)
                           └────3 years────┘
                          (time until callable)
```

**Key Concept**: All yield calculations start from **TODAY** (when you buy)
- YTC: From TODAY until call (3 years from now)
- YTM: From TODAY until maturity (15 years from now)
- The "5 years ago" is just background info (shows it's a seasoned bond)

**Student Understanding**: ✓ Clarified successfully

---

**Understanding Level**: EXCELLENT
- Correctly applied yesterday's pattern
- Performed calculations accurately
- Challenged instructor when numbers didn't match (critical thinking!)
- Understood timeline clarification

---

### Topic 2: Multi-Stage Dividend Discount Model (D.32)

**Topic**: D.32 Bond and stock valuation - Dividend Discount Model (DDM)

**Problem Given**: ABC Co. will pay dividends of $2, $0, $1 at end of Years 1, 2, 3 respectively. Future dividends (after Year 3) grow at 5% annually. Required return 9%. What is value per share?

**Options**:
- A) 18.60%
- B) 22.88% ✓
- C) 26.25%
- D) 28.86%

**Note**: Answer choices show percentages but should be dollar values (likely formatting error in question)

**Student's Initial Understanding**:
- ✓ Knows Gordon Growth Model: P = D₁ ÷ (r - g)
- ✓ Identified **two stages**: Non-constant dividends (years 1-3), then constant growth
- ✓ Knows denominator is (9% - 5%) = 4%
- ✓ Recognized need to combine $2, $0, $1 with growth portion
- ❓ Confused about HOW to combine the parts

**Student's Quote**: "I remember if you have D1 divided by required return of 9% you get intrinsic value... but here there are three values 2, 0, 1, so there are two stages... I probably think 1.05 divided by (9% - 5%) = 4%... but how does that work together with the 2, 0, 1 I don't know"

---

**Teaching Approach - Building on What Student Knows**:

**Step 1: Value the Non-Constant Dividends (Years 1-3)**

Find **present value** of each dividend:

**Year 1**: $2 ÷ (1.09)¹ = **$1.83**

**Year 2**: $0 ÷ (1.09)² = **$0.00**

**Year 3**: $1 ÷ (1.09)³ = **$0.77**

**Total PV of Years 1-3** = $1.83 + $0 + $0.77 = **$2.60**

---

**Step 2: Value ALL Future Dividends After Year 3**

**KEY INSIGHT**: After Year 3, dividends grow at 5% forever

**Year 4 dividend**:
- Year 3 dividend: $1
- Year 4 dividend: $1 × 1.05 = **$1.05**

**Use Gordon Growth Model at END of Year 3**:

**Value at Year 3** = D₄ ÷ (r - g)
- = $1.05 ÷ (0.09 - 0.05)
- = $1.05 ÷ 0.04
- = **$26.25** ← This is the "terminal value"

**IMPORTANT**: This $26.25 is the value **at the end of Year 3**, not today!

**Bring it back to TODAY** (present value):

**PV of terminal value** = $26.25 ÷ (1.09)³
- = $26.25 ÷ 1.295
- = **$20.27**

---

**Step 3: Add Them Together**

**Total Stock Value TODAY** = PV of Years 1-3 + PV of terminal value

**Stock Value = $2.60 + $20.27 = $22.87** ≈ **$22.88**

---

**The Answer: B) $22.88** (or 22.88% if format is weird)

---

**Visual Timeline Provided**:

```
TODAY          Year 1      Year 2      Year 3      Year 4...∞
  |              |           |           |           |
  |           $2 div      $0 div      $1 div    $1.05 div
  |              |           |           |       (grows 5%)
  |              |           |           |
  └──PV $1.83────┘           |           |
                 └──PV $0────┘           |
                             └──PV $0.77─┘
                                         |
                                    Terminal Value
                                    = $1.05 / 0.04
                                    = $26.25
                                    PV = $20.27

Total = $1.83 + $0 + $0.77 + $20.27 = $22.87
```

---

**The Formula Pattern Taught**:

**Multi-Stage DDM**:

**P₀ = [D₁/(1+r)¹] + [D₂/(1+r)²] + [D₃/(1+r)³] + [P₃/(1+r)³]**

Where **P₃ = D₄/(r-g)** ← This is the Gordon Growth part!

---

**Key Concepts Mastered**:

1. **Two-stage valuation**: Non-constant dividends + constant growth
2. **PV each non-constant dividend** separately
3. **Terminal value** = First constant-growth dividend ÷ (r - g)
4. **Discount terminal value** back to present
5. **Add all PVs** together for total stock value

---

**Understanding Level**: VERY GOOD
- Had right concepts but unclear on execution
- Understood after step-by-step walkthrough
- Grasped the "terminal value at Year 3, then discount back" concept

---

### Topic 3: Investment Risk Types - Physical Gold Liquidity (D.28)

**Topic**: D.28 Types of investment risk - Liquidity risk

**Problem Given**: Which type of risk is an individual most subject to when investing in physical gold?

**Options**:
- A) Liquidity ✓
- B) Commodities
- C) Exchange rate
- D) Constructive receipt

**Student's Response**: "I cannot sell it quickly, so liquidity is going to be a major issue here" ✓ **CORRECT**

**Student's Question**: "I don't know what constructive receipt means"

---

**Correct Answer: A) Liquidity**

**Student's Reasoning** (EXCELLENT):
- ✓ Identified physical gold (can buy at Costco)
- ✓ Recognized difficulty selling quickly
- ✓ Concluded liquidity is major issue

**Teaching - Why Liquidity Risk is Highest for Physical Gold**:

**What is Liquidity Risk?**
- Risk that you **can't sell an asset quickly** at a fair price
- Or you must accept big discount to sell fast

**Physical Gold Problems**:
- ✗ Can't sell instantly (need to find buyer)
- ✗ Verification needed (is it real gold?)
- ✗ Transportation required (physical delivery)
- ✗ Price negotiation (dealers lowball you)
- ✗ Huge bid-ask spread (buy $2,000/oz, sell $1,800/oz)
- ✗ No market hours (can't sell at 2am)

**Student's Costco Example Applied**:
- Buy gold bar at Costco for $2,100
- Emergency happens, need cash NOW
- Pawn shop offers $1,700 (big discount!)
- Or wait days/weeks for better buyer
- **This is liquidity risk!**

---

**Comparison Taught**:

**Physical Gold** (bars, coins):
- **High liquidity risk** ✗
- Takes days to sell
- Big bid-ask spread

**Gold ETF** (like GLD):
- **Low liquidity risk** ✓
- Sell in seconds during market hours
- Tiny spread (pennies)

---

**Why NOT the Other Answers**:

**B) Commodities** ❌
- "Commodities" is NOT a type of risk - it's an **asset class**!
- Like saying "stock risk" or "bond risk" - doesn't make sense
- Risk types: Liquidity, Credit, Market, Interest Rate, etc.

**C) Exchange Rate** ❌
- Exchange rate risk = currency values change
- Applies to foreign investments (Japanese stocks → yen risk)
- Gold is priced in **dollars** in U.S.
- Buy in dollars, sell in dollars
- **No exchange rate risk**

**D) Constructive Receipt** ❌
- **TAX CONCEPT**, not investment risk!
- Income is taxable when you have **right to access it**
- Example: December paycheck ready Dec 31, don't pick up until Jan 2
- Still taxable in December (constructive receipt)
- Completely irrelevant to gold investing!

---

**Asset Liquidity Ranking Taught**:

**Most Liquid** → **Least Liquid**:
1. Cash
2. Money market funds
3. Stocks (large cap)
4. Bonds (Treasury, corporate)
5. Mutual funds
6. Real estate
7. **Physical gold, art, collectibles** ← LEAST liquid

**Physical assets** = **HIGH liquidity risk**

---

**Real-World Example Provided**:

**Scenario**: Own $50,000 in gold bars, need $50,000 cash tomorrow for emergency

**Option 1 - Sell to dealer**:
- Dealer offers $45,000 (10% discount)
- Get cash fast but lose $5,000
- **Liquidity risk cost = $5,000!**

**Option 2 - Find best price**:
- Post online, wait for private buyer
- Get $49,000 (better price)
- Takes 2 weeks - too late!
- **Liquidity risk = can't access money when needed**

**If you had $50K in stock ETF**:
- Sell in 2 seconds
- Get $49,950 (tiny $50 spread)
- Cash in 2 days
- **Low liquidity risk!**

---

**Understanding Level**: EXCELLENT
- Correctly identified answer immediately
- Good intuition about physical asset problems
- Learned tax concept (constructive receipt) vs investment risk distinction

---

### Topic 4: Options vs Futures - Comprehensive Comparison (D.27)

**Topic**: D.27 Investment vehicles - Derivatives (Options and Futures)

**Student's Request**: "Tell me about the difference between options and futures... I remember one is more like a longer version, the other is shorter version, but I don't remember exact details"

**Student's Initial Understanding**:
- ✓ Knows calls vs puts (call = expect up, put = expect down)
- ✓ Understands basic option mechanics
- ❓ Doesn't know what futures contracts are
- ❓ Heard "obligation vs rights" but unclear
- **Focus requested**: Options vs Futures comparison

**Small Correction Made**: Student said "PUDs" - clarified meant "PUTS"

---

**Teaching Approach - The #1 Most Important Difference**:

## OBLIGATION vs. RIGHT

**OPTIONS** = You have a **RIGHT** (not obligation)
- You **CAN** exercise if you want
- You **CAN** let it expire worthless
- You **choose** what to do

**FUTURES** = You have an **OBLIGATION** (must do it!)
- You **MUST** buy or sell at contract expiration
- You **CANNOT** just walk away
- Both parties are **obligated** to execute

---

**Examples Provided**:

### CALL OPTION Example:

**You buy a call option**:
- Strike price: $50
- Stock currently: $45
- Premium paid: $3

**Scenario 1 - Stock goes to $60**:
- ✓ Exercise! Buy at $50, sell at $60
- Profit = $60 - $50 - $3 = $7 per share

**Scenario 2 - Stock drops to $30**:
- ✗ Don't exercise! (Stupid to buy at $50 when market is $30)
- Let option expire worthless
- Loss = $3 premium only (limited loss!)

**Key**: You had a **CHOICE** ← This is option's power!

---

### FUTURES CONTRACT Example:

**You buy futures contract** (agree to buy corn):
- Contract: Buy 5,000 bushels at $5/bushel in 3 months
- Total obligation: $25,000

**Scenario 1 - Corn price goes to $7/bushel**:
- ✓ Great! You buy at $5, market is $7
- Profit = ($7 - $5) × 5,000 = $10,000

**Scenario 2 - Corn price drops to $3/bushel**:
- ✗ **You STILL must buy at $5!** (obligation!)
- Market is $3, you pay $5
- Loss = ($5 - $3) × 5,000 = $10,000 loss!
- **You can't walk away!**

**Key**: You had **NO CHOICE** ← This is futures' risk!

---

**Comprehensive Comparison Table**:

| Feature | **OPTIONS** | **FUTURES** |
|---------|-------------|-------------|
| **Nature** | **RIGHT** to buy/sell | **OBLIGATION** to buy/sell |
| **Upfront Cost** | Pay **premium** | No premium, but **margin** required |
| **Max Loss (buyer)** | **Premium only** (limited) | **Unlimited** |
| **Flexibility** | Can choose not to exercise | **Must** execute contract |
| **Expiration** | Various (weeks to years) | Specific dates (quarterly) |
| **Standardization** | Some customization possible | Highly standardized |
| **Primary Use** | Speculation, hedging | Hedging, price locking |
| **Typical Investor** | Individual investors, smaller | Institutional, businesses, commodities |

---

**The Premium Difference (CRITICAL)**:

### OPTIONS - You Pay a Premium

**Call option example**:
- Pay $3 per share premium **UPFRONT**
- This is your **maximum loss**
- If stock drops, you lose $3, that's it!

### FUTURES - No Premium BUT Margin Required

**Futures contract**:
- **Don't pay premium**
- Must deposit **margin** (security deposit)
- Margin typically 5-15% of contract value
- **But loss can be unlimited!**

**Example**:
- Futures contract: $100,000 value
- Margin required: $10,000 (10%)
- Position moves against you by 20%:
  - Loss = $20,000 (more than margin!)
  - Must add more money or be liquidated

---

**Real-World Use Cases**:

### Who Uses OPTIONS?

**Individual investors**:
- "I think Tesla will go up, let me buy a call"
- Limited risk ($3 premium)
- Can't lose more than premium

**Conservative investors**:
- Protective puts (insurance on stocks)
- Covered calls (income generation)

---

### Who Uses FUTURES?

**Farmers** (hedging):
- Plant corn in April
- Want to lock in price NOW for September harvest
- Sell futures contract at $5/bushel
- Guaranteed price regardless of market
- **This is hedging, not speculation!**

**Airlines** (hedging):
- Need jet fuel for next year
- Worried fuel prices will spike
- Buy futures to lock in price
- **Protects business from price swings**

**Speculators**:
- Day traders betting on commodities
- High leverage (control $100K with $10K margin)
- **Very risky!**

---

**Key Exam Distinctions**:

**OPTIONS**:
- ✓ Limited loss (premium only)
- ✓ More flexibility
- ✓ Good for individual investors
- ✗ Premium can be expensive
- ✗ Time decay (expire worthless if not exercised)

**FUTURES**:
- ✓ No premium upfront
- ✓ Highly liquid markets
- ✓ Perfect for hedging business risk
- ✗ **Unlimited loss potential**
- ✗ Obligation (can't walk away)
- ✗ Margin calls (must add money if position moves)

---

**Memory Tricks Taught**:

**OPTIONS** = "**OP**tional" = You have a choice
- Like having a **coupon** - you CAN use it, but don't have to

**FUTURES** = "**FU**lly committed" = You must do it
- Like signing a **contract** to buy a house - you MUST close

---

**Comprehension Check Questions Given** (for next session):

1. You buy a call option for $5 premium (strike $100). Stock drops to $50. What's your maximum loss?

2. You enter a futures contract to buy oil at $80/barrel. Oil drops to $60. Can you just walk away and lose nothing?

3. Which is riskier for an individual investor - buying a call option or buying a futures contract? Why?

---

**Understanding Level**: EXCELLENT
- Student had good foundation on options (calls/puts)
- Completely new to futures concept
- Grasped the critical "right vs obligation" distinction
- Understood premium vs margin difference
- Appreciated real-world use case examples

---

## Topics Covered Today

| Topic | CFP Code | Confidence | Notes |
|-------|----------|------------|-------|
| Bond Yield Rankings (Review) | D.32 | High | Perfect application of yesterday's pattern |
| YTC Approximation Formula | D.32 | High | Learned proper calculation method |
| Timeline Clarification | D.32 | High | Understood "from today" concept |
| Multi-Stage Dividend Discount Model | D.32 | Medium-High | New concept, needs practice |
| Liquidity Risk - Physical Gold | D.28 | High | Excellent intuition demonstrated |
| **Options vs Futures** | **D.27** | **Medium-High** | **NEW - Comprehensive understanding** |

---

## Key Concepts Mastered

### Bond Yield Rankings - Verification (D.32)
- **Discount bond pattern**: CR < CY < YTM < YTC ✓ retained from yesterday
- **YTC approximation formula**: [Coupon + (Call Price - Current Price)/Years] / [(Call Price + Current Price)/2]
- **Timeline clarity**: All yields calculated from TODAY, not from issuance
- Perfect execution on practice problem

### Multi-Stage Dividend Discount Model (D.32)
- **Step 1**: PV each non-constant dividend separately
- **Step 2**: Calculate terminal value at end of non-constant period (P₃ = D₄/(r-g))
- **Step 3**: Discount terminal value back to present
- **Step 4**: Add all PVs together
- **Formula**: P₀ = Σ[Dₜ/(1+r)ᵗ] + [Pₙ/(1+r)ⁿ]
- Example: $2, $0, $1 then 5% growth → $22.88 value

### Liquidity Risk (D.28)
- **Definition**: Can't sell quickly at fair price
- **Physical gold**: HIGH liquidity risk (days to sell, big spread)
- **Gold ETF**: LOW liquidity risk (seconds to sell, tiny spread)
- **Asset liquidity ranking**: Cash → Stocks → Bonds → Real Estate → Physical assets (least liquid)
- **Not investment risks**: Commodities (asset class), Constructive receipt (tax concept)

### Options vs Futures - Complete Comparison (D.27)

**The #1 Difference - Obligation vs Right**:
- **Options**: RIGHT to buy/sell (can choose not to exercise)
- **Futures**: OBLIGATION to buy/sell (must execute)

**Cost Structure**:
- **Options**: Pay premium upfront (max loss = premium)
- **Futures**: No premium, but margin required (loss can be unlimited)

**Risk Profile**:
- **Options**: Limited downside (premium only)
- **Futures**: Unlimited downside (must honor contract)

**Typical Users**:
- **Options**: Individual investors, speculation, protective strategies
- **Futures**: Businesses hedging, farmers, airlines, speculators

**Memory Tricks**:
- Options = "OPtional" (have choice, like coupon)
- Futures = "FUlly committed" (must do it, like house contract)

**Real-World Examples**:
- Farmer sells corn futures (locks in harvest price)
- Airline buys fuel futures (protects from price spikes)
- Individual buys call option (limited risk speculation)

---

## Progress Assessment

**Topics Reinforced**:
- D.32 Bond valuation (yield rankings, YTC calculation)
- D.28 Investment risk (liquidity risk identification)

**New Topics Added**:
- D.32 Multi-stage dividend discount model (DDM)
- D.27 Options vs Futures (derivatives comparison)

**Strengths Observed**:
- Excellent retention from previous session (bond yield rankings)
- Strong critical thinking (challenged instructor's numbers - was right!)
- Good intuition (physical gold liquidity)
- Quick learner (grasped futures obligation concept immediately)
- Asked clarifying questions (timeline for YTC)

**Areas for Continued Practice**:
- Multi-stage DDM calculations (needs more practice problems)
- Options strategies (covered calls, protective puts)
- Futures margin and leverage calculations

---

## Session Statistics

**Session Duration**: ~60 minutes
**Topics Covered**: 4 major topics (bond yields review, DDM, liquidity risk, options vs futures)
**Format**: Mixed (practice testing + new concept teaching)
**Performance**: Excellent - strong retention, good intuition, quick learning

**Days Until Exam**: 16 days

---

## Notes

**Day 6 of Study Plan - October 25, 2025**

Mixed session combining practice problem verification (testing yesterday's learning) with new concept introduction. Student demonstrated excellent retention of bond yield rankings and strong critical thinking by challenging instructor calculations.

**Major Learning Achievements**:
- Verified bond yield ranking pattern retention (discount bonds)
- Learned proper YTC approximation formula
- Mastered multi-stage dividend discount model
- Identified liquidity risk correctly with good reasoning
- **Comprehensively understood Options vs Futures distinction**

**Critical Thinking Demonstrated**:
- Challenged instructor on YTC calculation discrepancy (7.8% vs 10.2%)
- Asked excellent clarifying question about timeline (5 years ago + 3 years)
- Correctly identified liquidity as main risk for physical gold

**Key Pattern Reinforced**:
- All yield calculations start from TODAY (purchase date)
- Terminal value in DDM must be discounted back to present
- Physical assets have highest liquidity risk

**Ready for**: Continue D.27 (investment vehicles - stocks, bonds, mutual funds, REITs) or move to D.30-D.31 (quantitative concepts)

**Investment Planning Progress**: 7/9 topics (78%) - nearing completion!

---

**Session Status**: COMPLETE - Ready to save
