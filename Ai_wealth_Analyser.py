import os, sys, time, shutil, datetime, threading
import numpy as np

# ─── ANSI ──────────────────────────────────────────────────────
R    = "\033[0m";  B = "\033[1m";  IT = "\033[3m"
def fg(r,g,b): return f"\033[38;2;{r};{g};{b}m"

CYAN  = fg(0,212,255);  GOLD  = fg(255,215,0)
GREEN = fg(0,255,136);  RED   = fg(255,68,102)
ORAN  = fg(255,140,0);  SKY   = fg(135,206,235)
GRAY  = fg(120,120,120);WHITE = fg(210,210,210)
PINK  = fg(255,105,180);TEAL  = fg(0,200,180)

W = min(shutil.get_terminal_size((100,40)).columns, 110)

def clear(): os.system("cls" if os.name=="nt" else "clear")

def clen(s):
    out=""; i=0
    while i<len(s):
        if s[i]=="\033": j=s.index("m",i); i=j+1
        else: out+=s[i]; i+=1
    return len(out)

def center(t): print(" "*max(0,(W-clen(t))//2)+t)

def rule(char="─", color=CYAN, label=""):
    if label:
        s=max(0,(W-clen(label)-2)//2)
        print(f"{color}{char*s} {B}{label}{R}{color} {char*(W-s-clen(label)-2)}{R}")
    else:
        print(f"{color}{char*W}{R}")

def box(lines, title="", color=CYAN):
    w=W-2
    if title:
        t=f" {B}{GOLD}{title}{R}{color} "
        print(f"{color}╔═{t}{'═'*(w-clen(title)-3)}╗{R}")
    else:
        print(f"{color}╔{'═'*w}╗{R}")
    for ln in lines:
        p=w-clen(ln)-2
        print(f"{color}║{R} {ln}{' '*max(0,p)} {color}║{R}")
    print(f"{color}╚{'═'*w}╝{R}")

def spinner(label, fn, *args, **kwargs):
    frames=["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    done=[False]; res=[None]
    def _r(): res[0]=fn(*args,**kwargs); done[0]=True
    t=threading.Thread(target=_r,daemon=True); t.start()
    i=0
    while not done[0]:
        print(f"\r  {CYAN}{frames[i%10]}{R}  {WHITE}{label}...{R}   ",end="",flush=True)
        time.sleep(0.08); i+=1
    print(f"\r  {GREEN}+{R}  {WHITE}{label}{R}                   ")
    return res[0]

def ask(prompt, default="", cast=float):
    d=f"{default:,.0f}" if cast==float and default!="" else str(default)
    line=f"  {CYAN}>{R}  {WHITE}{prompt}{R}  {GRAY}[{d}]{R}  {GOLD}:{R} " if default!="" \
         else f"  {CYAN}>{R}  {WHITE}{prompt}{R}  {GOLD}:{R} "
    while True:
        raw=input(line).strip()
        if raw=="" and default!="": return cast(default) if cast else default
        try:    return cast(raw.replace(",",""))
        except: print(f"  {RED}Invalid, try again.{R}")

def ask_choice(prompt, choices):
    for i,c in enumerate(choices,1): print(f"    {GOLD}{i}{R}  {WHITE}{c}{R}")
    while True:
        raw=input(f"\n  {CYAN}>{R}  {WHITE}{prompt}{R}  {GOLD}:{R} ").strip()
        if raw.isdigit() and 1<=int(raw)<=len(choices): return int(raw)-1, choices[int(raw)-1]
        print(f"  {RED}Enter 1-{len(choices)}{R}")

def fmt(v):
    if abs(v)>=1e7: return f"Rs{v/1e7:.2f}Cr"
    if abs(v)>=1e5: return f"Rs{v/1e5:.2f}L"
    return f"Rs{v:,.0f}"

def si(v):
    if abs(v)>=1e7: return f"{v/1e7:.1f}Cr"
    if abs(v)>=1e5: return f"{v/1e5:.0f}L"
    if abs(v)>=1e3: return f"{v/1e3:.0f}K"
    return f"{v:.0f}"

# ─── CONSTANTS ─────────────────────────────────────────────────
INFLATION  = 0.062
MONTE_RUNS = 1000
CW         = min(W-10, 76)   # chart usable width

PROFILES={
    "Conservative  (Bonds/FD)":  dict(mu=0.065,sigma=0.020,color=TEAL),
    "Moderate      (Balanced)":  dict(mu=0.100,sigma=0.060,color=GREEN),
    "Aggressive    (Equity/MF)": dict(mu=0.145,sigma=0.140,color=GOLD),
    "High-Risk     (Crypto)":    dict(mu=0.220,sigma=0.400,color=RED),
}
PNAMES=list(PROFILES.keys())

EXPENSE_CATS=[
    ("Housing (rent/EMI)",       "housing"),
    ("Food & Groceries",         "food"),
    ("Transport",                "transport"),
    ("Healthcare & Insurance",   "healthcare"),
    ("Education",                "education"),
    ("Entertainment & Dining",   "entertainment"),
    ("Clothing & Personal Care", "clothing"),
    ("Subscriptions/Utilities",  "utilities"),
    ("Loan Repayments",          "loans"),
    ("Gifts & Misc",             "misc"),
]

# ─── BANNER ────────────────────────────────────────────────────
def show_banner():
    clear()
    L=[
        f"{CYAN}  ___  ___   _    _ ___  _   _   _____  _   _ {R}",
        f"{CYAN} / _ \| \ \ / /  | '__ \| | | | |_   _|| | | |{R}",
        f"{CYAN}| |_| |  \ V /   | |  | | |_| |   | |  | |_| |{R}",
        f"{CYAN} \___/|   \_/    |_|  |_|\___/    |_|   \___/ {R}",
        f"{GOLD}      W E A L T H   V I S U A L I S E R       {R}",
    ]
    print()
    for l in L: center(l)
    print()
    center(f"{B}{GOLD}>> AI-POWERED  BUDGET ANALYSIS & WEALTH PREDICTION <<{R}")
    center(f"{GRAY}100% Terminal  |  Monte Carlo Simulation  |  Market Trends{R}")
    print(); rule("=",CYAN); print()

# ─── COLLECT ───────────────────────────────────────────────────
def collect_income():
    rule("-",GOLD,"  STEP 1 of 4 -- ANNUAL INCOME  ")
    print(f"  {GRAY}Press Enter to use defaults shown in [brackets].{R}\n")
    d={}
    d["salary"]    = ask("Salary / Business Income    (Rs/yr)", 600000)
    d["freelance"] = ask("Freelance / Side-hustle     (Rs/yr)", 0)
    d["rental"]    = ask("Rental Income               (Rs/yr)", 0)
    d["other"]     = ask("Other Income                (Rs/yr)", 0)
    d["total"]     = sum(v for k,v in d.items() if k!="total")
    print(f"\n  {GREEN}+  Total Annual Income  >>  {B}{fmt(d['total'])}{R}\n")
    return d

def collect_expenses():
    rule("-",GOLD,"  STEP 2 of 4 -- ANNUAL EXPENSES  ")
    print(f"  {GRAY}Enter yearly totals (monthly x 12 is fine).{R}\n")
    d={}
    for label,key in EXPENSE_CATS: d[key]=ask(f"{label:<32}(Rs/yr)",0)
    d["total"]=sum(v for k,v in d.items() if k!="total")
    print(f"\n  {RED}x  Total Annual Expenses  >>  {B}{fmt(d['total'])}{R}\n")
    return d

def collect_assets_goals():
    rule("-",GOLD,"  STEP 3 of 4 -- ASSETS & GOALS  ")
    print()
    a={}
    a["savings"]     = ask("Current Savings / FD        (Rs)", 50000)
    a["investments"] = ask("Investments (MF/stocks)     (Rs)", 0)
    a["property"]    = ask("Property Value              (Rs)", 0)
    a["other"]       = ask("Other Assets                (Rs)", 0)
    a["total"]       = sum(a.values())
    print()
    g={}
    g["target"]      = ask("Retirement Corpus Target    (Rs)", 10_000_000)
    g["retire_age"]  = int(ask("Target Retirement Age          ", 60, cast=int))
    g["current_age"] = int(ask("Your Current Age               ", 30, cast=int))
    g["years"]       = max(1,g["retire_age"]-g["current_age"])
    print(f"\n  {SKY}You have {B}{g['years']} years{R}{SKY} to reach your goal.{R}\n")
    return a,g

def choose_profile():
    rule("-",GOLD,"  STEP 4 of 4 -- INVESTMENT PROFILE  ")
    print()
    print(f"  {GOLD}{'#':<3}{R}  {WHITE}{'Profile':<36}{R}  {GREEN}{'CAGR':>8}{R}  {RED}{'Risk':>6}{R}")
    print(f"  {GRAY}{'---'}  {'---'*12}  {'------'}  {'----'}{R}")
    for i,(n,p) in enumerate(PROFILES.items(),1):
        print(f"  {GOLD}{i}{R}  {p['color']}{n:<36}{R}  {GREEN}{p['mu']*100:>7.1f}%{R}  {RED}{p['sigma']*100:>4.0f}%{R}")
    idx,name=ask_choice("Choose profile (1-4)",PNAMES)
    prof=PROFILES[name]
    print(f"\n  {GREEN}+  Selected >>  {B}{prof['color']}{name.strip()}{R}\n")
    return name,prof

# ─── CALCULATIONS ──────────────────────────────────────────────
def analyse(inc,exp,assets,goals,prof):
    surplus=inc["total"]-exp["total"]
    sr=surplus/inc["total"]*100 if inc["total"] else 0
    r,yrs=prof["mu"],goals["years"]
    P0=assets["investments"]+assets["savings"]
    ai=max(0,surplus*0.70)
    fv_l=P0*(1+r)**yrs
    fv_a=ai*((1+r)**yrs-1)/r*(1+r) if r>0 else ai*yrs
    proj=fv_l+fv_a
    target=goals["target"]
    gap=max(0,target-proj)
    inf_exp=exp["total"]*(1+INFLATION)**yrs
    swr_mo=proj*0.04/12
    mr,mo=r/12,yrs*12
    sip=(target-fv_l)*mr/((1+mr)**mo-1) if mr>0 and mo>0 else (target-P0)/(yrs*12) if yrs else 0
    return dict(surplus=surplus,mo_surplus=surplus/12,sr=sr,
                fv_l=fv_l,fv_a=fv_a,proj=proj,target=target,
                gap=gap,inf_exp=inf_exp,swr_mo=swr_mo,sip=sip,ai=ai)

def monte_carlo(inc,exp,assets,goals,prof):
    P0=assets["investments"]+assets["savings"]
    ai=max(0,(inc["total"]-exp["total"])*0.70)
    yrs=goals["years"]
    rng=np.random.default_rng(42)
    paths=np.zeros((MONTE_RUNS,yrs+1))
    paths[:,0]=P0
    for y in range(1,yrs+1):
        r=rng.normal(prof["mu"],prof["sigma"],MONTE_RUNS)
        paths[:,y]=paths[:,y-1]*(1+r)+ai
    return paths

# ─── TERMINAL CHART HELPERS ────────────────────────────────────
BLOCKS=" ▁▂▃▄▅▆▇█"
CH=12   # chart height rows

def sparkline(values,color=CYAN,width=None):
    w=width or CW
    step=max(1,len(values)//w)
    pts=values[::step][:w]
    mn,mx=min(pts),max(pts); rng=mx-mn if mx!=mn else 1
    return color+"".join(BLOCKS[int((v-mn)/rng*8)] for v in pts)+R

def hbar(val,total,width=40,color=GREEN):
    pct=min(1.0,val/total) if total else 0
    f=int(pct*width)
    return f"{color}{'|'*f}{GRAY}{'.'*(width-f)}{R}  {color}{pct*100:5.1f}%{R}"

def vbar_chart(title,labels,values,color=CYAN):
    """Vertical bar chart drawn in terminal."""
    print(f"\n  {B}{GOLD}{title}{R}")
    rule("-",GRAY)
    if not values or max(values)==0:
        print(f"  {GRAY}(no data){R}\n"); return
    max_v=max(values)
    bar_w=max(2,min(8,(CW-4)//(len(values)+1)))
    for row in range(CH,0,-1):
        thresh=max_v*row/CH
        if row==CH: yl=f"{GRAY}{si(max_v):>6}{R} |"
        elif row==CH//2: yl=f"{GRAY}{si(max_v/2):>6}{R} |"
        elif row==1: yl=f"{GRAY}{'0':>6}{R} |"
        else: yl=f"       |"
        line=""
        for v in values:
            blk = f"{color}{'#'*bar_w}{R}" if v>=thresh else f"{GRAY}{'.'*bar_w}{R}"
            line+=blk+" "
        print(f"  {yl}{line}")
    # x-axis
    print("  "+"       +"+("-"*(bar_w+1))*len(values))
    xline="         "
    for lb in labels:
        s=lb[:bar_w]; xline+=f"{GRAY}{s:<{bar_w+1}}{R}"
    print(xline+"\n")

def line_chart_ascii(title,series_list,year_labels,height=CH):
    """Multi-series line chart with ASCII grid."""
    print(f"\n  {B}{GOLD}{title}{R}")
    rule("-",GRAY)
    all_vals=[v for s in series_list for v in s["values"]]
    if not all_vals: print(f"  {GRAY}(no data){R}\n"); return
    mn,mx=min(all_vals),max(all_vals); rng=mx-mn if mx!=mn else 1

    def to_row(v): return int((v-mn)/rng*(height-1))

    grid=[[" "]*CW for _ in range(height)]
    for s in series_list:
        vals=s["values"]; col=s["color"]; sym=s.get("sym","*")
        for i,v in enumerate(vals):
            x=int(i*CW/len(vals)); y=to_row(v)
            if 0<=x<CW and 0<=y<height: grid[y][x]=f"{col}{sym}{R}"

    for row in range(height-1,-1,-1):
        v_here=mn+rng*row/(height-1)
        if row in (height-1,height//2,0):
            prefix=f"{GRAY}{si(v_here):>6}{R}|"
        else:
            prefix=f"      |"
        print("  "+prefix+"".join(grid[row]))
    # x-axis
    print("  "+"      +"+"-"*CW)
    n=len(year_labels)
    xs=f"       {GRAY}{year_labels[0]}{R}"
    xs+=" "*max(0,CW//3-6)+f"{GRAY}{year_labels[n//3] if n//3<n else ''}{R}"
    xs+=" "*max(0,CW//3-6)+f"{GRAY}{year_labels[2*n//3] if 2*n//3<n else ''}{R}"
    xs+=" "*max(0,CW//4)+f"{GRAY}{year_labels[-1]}{R}"
    print("  "+xs+"\n")

# ─── DISPLAY SECTIONS ──────────────────────────────────────────
def show_budget_overview(inc,exp,res):
    rule("=",CYAN,"  BUDGET OVERVIEW  ")
    print()

    # Income bars
    print(f"  {B}{GOLD}Income Breakdown{R}")
    rule("-",GRAY)
    for label,key in [("Salary","salary"),("Freelance","freelance"),
                      ("Rental","rental"),("Other","other")]:
        v=inc.get(key,0)
        if v>0:
            print(f"  {WHITE}{label:<20}{R}  {hbar(v,inc['total'],36,CYAN)}  {GRAY}{fmt(v)}{R}")
    print()

    # Expense bars
    print(f"  {B}{GOLD}Expense Breakdown{R}")
    rule("-",GRAY)
    for label,key in EXPENSE_CATS:
        v=exp.get(key,0)
        if v>0:
            print(f"  {WHITE}{label:<28}{R}  {hbar(v,exp['total'],28,RED)}  {GRAY}{fmt(v)}{R}")
    print()

    # Surplus / deficit bar
    sc=GREEN if res["surplus"]>=0 else RED
    lbl="SURPLUS" if res["surplus"]>=0 else "DEFICIT"
    pct=abs(res["surplus"])/inc["total"] if inc["total"] else 0
    f=int(pct*50); bar=f"{sc}{'|'*f}{GRAY}{'.'*(50-f)}{R}"
    print(f"  {B}{GOLD}{lbl}{R}  {bar}  {sc}{B}{fmt(res['surplus'])}{R}  {GRAY}({res['sr']:.1f}%){R}\n")

def show_wealth_projection(inc,exp,assets,goals,prof,res):
    rule("=",CYAN,"  WEALTH PROJECTION  ")

    yr=list(range(goals["years"]+1))
    r=prof["mu"]; P0=assets["investments"]+assets["savings"]; ai=res["ai"]
    corp=[P0*(1+r)**y for y in yr]
    ann=[ai*((1+r)**y-1)/r*(1+r) if r>0 else ai*y for y in yr]
    tot=[c+a for c,a in zip(corp,ann)]
    inf=[exp["total"]*(1+INFLATION)**y for y in yr]
    tgt=[goals["target"]]*len(yr)
    cur_yr=datetime.date.today().year
    ylabels=[cur_yr+y for y in yr]

    series=[
        dict(values=tot, color=CYAN,  sym="#"),
        dict(values=corp,color=GREEN, sym="+"),
        dict(values=ann, color=GOLD,  sym="."),
        dict(values=inf, color=ORAN,  sym="~"),
        dict(values=tgt, color=RED,   sym="-"),
    ]
    line_chart_ascii("Projected Wealth Over Time",series,ylabels,height=14)
    print(f"  Legend:  {CYAN}# Total{R}  {GREEN}+ Corpus{R}  "
          f"{GOLD}. SIP{R}  {ORAN}~ Inf-Expenses{R}  {RED}- Target{R}\n")

    # Milestones
    print(f"  {B}{GOLD}Key Milestones{R}")
    rule("-",GRAY)
    print(f"  {GRAY}{'Year':<6}{'Age':<5}{'Wealth':>14}{'vs Target':>12}{'Inf-Expenses':>15}{R}")
    print(f"  {GRAY}{'----':<6}{'---':<5}{'------':>14}{'---------':>12}{'------------':>15}{R}")
    for y in sorted(set([1,5,10,goals["years"]//2,goals["years"]])):
        if y>goals["years"]: continue
        tw=tot[y]; pct=tw/goals["target"]*100 if goals["target"] else 0
        age=goals["current_age"]+y; ie=inf[y]
        c=GREEN if pct>=100 else GOLD if pct>=50 else RED
        print(f"  {WHITE}{y:<6}{age:<5}{R}{CYAN}{fmt(tw):>14}{R}{c}{pct:>10.1f}%{R}{GRAY}{fmt(ie):>15}{R}")
    print()

def show_monte_carlo(paths,goals):
    rule("=",CYAN,"  MONTE CARLO SIMULATION  ")
    yrs=paths.shape[1]-1
    p10=np.percentile(paths,10,axis=0)
    p25=np.percentile(paths,25,axis=0)
    p50=np.percentile(paths,50,axis=0)
    p75=np.percentile(paths,75,axis=0)
    p90=np.percentile(paths,90,axis=0)
    sp=(paths[:,-1]>=goals["target"]).mean()*100
    spc=GREEN if sp>=75 else GOLD if sp>=50 else RED

    print(f"\n  {B}{WHITE}{MONTE_RUNS:,} simulations  |  Target: {GOLD}{fmt(goals['target'])}{R}"
          f"  |  Success: {spc}{B}{sp:.1f}%{R}\n")

    # Percentile sparklines
    print(f"  {GRAY}{'Percentile':<16}Wealth Trend (sparkline){' '*(CW-25)}End Value{R}")
    rule("-",GRAY)
    for lbl,vals,col in [
        ("90th (best)",p90,GREEN),
        ("75th",       p75,TEAL),
        ("50th median",p50,CYAN),
        ("25th",       p25,GOLD),
        ("10th worst", p10,RED),
    ]:
        step=max(1,(yrs+1)//CW)
        pts=vals[::step][:CW]
        mn2,mx2=pts.min(),pts.max(); rng2=mx2-mn2 if mx2!=mn2 else 1
        spark=col+"".join(BLOCKS[int((v-mn2)/rng2*8)] for v in pts)+R
        ec=GREEN if vals[-1]>=goals["target"] else RED
        print(f"  {col}{lbl:<16}{R}{spark}  {ec}{fmt(vals[-1]):>10}{R}")

    # Distribution histogram
    print(f"\n  {B}{GOLD}Final Wealth Distribution (Year {yrs}){R}")
    rule("-",GRAY)
    final=paths[:,-1]; bins=min(30,CW//2)
    mn,mx=final.min(),final.max(); bsz=(mx-mn)/bins if mx!=mn else 1
    hist=[0]*bins
    for v in final:
        b=min(bins-1,int((v-mn)/bsz)); hist[b]+=1
    mh=max(hist); bw=max(1,CW//bins)
    for row in range(7,0,-1):
        line="  "
        for i,h in enumerate(hist):
            fill=h/mh>=row/7
            center_v=mn+i*bsz
            c=GREEN if center_v>=goals["target"] else CYAN
            line+=(f"{c}{'|'*bw}{R}" if fill else f"{GRAY}{'.'*bw}{R}")
        print(line)
    # x labels
    xline="  "
    for i in range(0,bins,max(1,bins//6)):
        lbl=si(mn+i*bsz); xline+=f"{GRAY}{lbl:<{bw*max(1,bins//6)}}{R}"
    print(xline)
    print(f"  {GRAY}Bars to the right of {si(goals['target'])} = SUCCESS scenarios.{R}\n")
    return sp

def show_profile_comparison(inc,exp,assets,goals):
    rule("=",CYAN,"  PROFILE COMPARISON  ")
    print(f"\n  {B}{GOLD}Final Wealth in {goals['years']} Years -- All Profiles{R}")
    rule("-",GRAY)
    P0=assets["investments"]+assets["savings"]
    ai=max(0,(inc["total"]-exp["total"])*0.70)
    yrs=goals["years"]; results={}; max_v=goals["target"]
    for name,p in PROFILES.items():
        r=p["mu"]; c=P0*(1+r)**yrs
        a=ai*((1+r)**yrs-1)/r*(1+r) if r>0 else ai*yrs
        tot=c+a; results[name]=tot; max_v=max(max_v,tot)

    for name,p in PROFILES.items():
        tot=results[name]; pct=tot/max_v
        f=int(pct*46)
        bar=f"{p['color']}{'|'*f}{GRAY}{'.'*(46-f)}{R}"
        hit=f"{GREEN}HIT{R}" if tot>=goals["target"] else f"{RED}SHORT{R}"
        print(f"  {p['color']}{name:<34}{R}  {bar}  {CYAN}{fmt(tot):>12}{R}  {hit}")

    # Target line marker
    tf=int(goals["target"]/max_v*46)
    print(f"  {RED}{'Target':<34}{R}  {RED}{'|':>{tf+2}}{R}  {RED}{fmt(goals['target']):>12}{R}")
    print()

    # Sparklines
    print(f"  {B}{GOLD}Growth Trends{R}")
    rule("-",GRAY)
    for name,p in PROFILES.items():
        r=p["mu"]
        vals=[P0*(1+r)**y + (ai*((1+r)**y-1)/r*(1+r) if r>0 else ai*y) for y in range(yrs+1)]
        step=max(1,len(vals)//(CW-14))
        pts=vals[::step][:CW-14]
        mn2,mx2=min(pts),max(pts); rng=mx2-mn2 if mx2!=mn2 else 1
        sp=p["color"]+"".join(BLOCKS[int((v-mn2)/rng*8)] for v in pts)+R
        print(f"  {p['color']}{name[:26]:<28}{R}  {sp}  {GRAY}{si(vals[0])} >> {si(vals[-1])}{R}")
    print()

def show_savings_meter(res):
    rule("=",CYAN,"  SAVINGS RATE ANALYSIS  ")
    sr=res["sr"]
    srlabel=("Below Average","FIRE Zone","Excellent","Good","Average")[
        (sr<10)*0 or (sr>=50)*1 or (sr>=35)*2 or (sr>=20)*3 or 4
    ]
    src=RED if sr<10 else GREEN if sr>=35 else GOLD
    print(f"\n  {B}{GOLD}Your Savings Rate:  {src}{B}{sr:.1f}%  --  {srlabel}{R}\n")

    rows=[
        (0,10,"Below Average (< 10%)",RED),
        (10,20,"Average (10-20%)",ORAN),
        (20,35,"Good (20-35%)",GOLD),
        (35,50,"Excellent (35-50%)",GREEN),
        (50,100,"FIRE Zone (> 50%)",CYAN),
    ]
    for lo,hi,lbl,col in rows:
        active=lo<=sr<hi or (hi==100 and sr>=lo)
        marker=f"  {B}<-- YOU{R}" if active else ""
        w=hi-lo; f=min(w,max(0,int((min(sr,hi)-lo))))*2 if active else w*2
        bar=f"{col}{'#'*f}{'.'*(w*2-f)}{R}"
        print(f"  {col}{lbl:<26}{R}  {bar}{marker}")
    print()

    print(f"  {B}{GOLD}Benchmark Comparison{R}")
    rule("-",GRAY)
    benches=[
        ("Average Indian household",12,GRAY),
        ("Recommended minimum",     20,GOLD),
        ("Wealth-building zone",    30,GREEN),
        (f"Your rate ({sr:.1f}%)",  sr, CYAN),
    ]
    for lbl,val,col in benches:
        f2=int(min(val,60)/60*40)
        bar=f"{col}{'|'*f2}{'.'*(40-f2)}{R}"
        print(f"  {WHITE}{lbl:<28}{R}  {bar}  {col}{val:.1f}%{R}")
    print()

def show_summary_box(inc,exp,assets,goals,pname,prof,res,sp):
    rule("=",GOLD,"  FULL ANALYSIS SUMMARY  ")
    sc=GREEN if res["surplus"]>=0 else RED
    gc=GREEN if res["gap"]==0 else RED
    spc=GREEN if sp>=75 else GOLD if sp>=50 else RED
    pct=min(1.0,res["proj"]/res["target"]) if res["target"] else 1.0
    f=int(pct*28); bar=f"{GREEN}{'#'*f}{GRAY}{'.'*(28-f)}{R}  {GOLD}{pct*100:.0f}%{R}"
    box([
        f"  {GRAY}--- CASHFLOW -----------------------------------{R}",
        f"  {GRAY}Total Annual Income       {R}{GREEN}{B}{fmt(inc['total']):>16}{R}",
        f"  {GRAY}Total Annual Expenses     {R}{RED}{B}{fmt(exp['total']):>16}{R}",
        f"  {GRAY}Annual Surplus            {R}{sc}{B}{fmt(res['surplus']):>16}{R}",
        f"  {GRAY}Monthly Surplus           {R}{WHITE}{fmt(res['mo_surplus']):>16}{R}",
        f"  {GRAY}Savings Rate              {R}{GOLD}{B}{res['sr']:>14.1f}%{R}",
        "",
        f"  {GRAY}--- NET WORTH ----------------------------------{R}",
        f"  {GRAY}Current Net Worth         {R}{CYAN}{fmt(assets['total']):>16}{R}",
        f"  {GRAY}Annual Amount Invested    {R}{GOLD}{fmt(res['ai']):>16}{R}",
        "",
        f"  {GRAY}--- PROJECTION ---------------------------------{R}",
        f"  {GRAY}Projected Wealth          {R}{CYAN}{B}{fmt(res['proj']):>16}{R}",
        f"  {GRAY}Target Corpus             {R}{WHITE}{fmt(res['target']):>16}{R}",
        f"  {GRAY}Progress to Target        {R}  {bar}",
        f"  {GRAY}Shortfall                 {R}{gc}{'On track!' if res['gap']==0 else fmt(res['gap']):>16}{R}",
        f"  {GRAY}Inf-adj Annual Expenses   {R}{ORAN}{fmt(res['inf_exp']):>16}{R}",
        f"  {GRAY}Sustainable Monthly Draw  {R}{GREEN}{fmt(res['swr_mo']):>16}{R}",
        "",
        f"  {GRAY}--- ACTION ITEMS --------------------------------{R}",
        f"  {GRAY}Required Monthly SIP      {R}{PINK}{B}{fmt(res['sip']):>16}{R}",
        f"  {GRAY}Investment Profile        {R}{WHITE}{pname.strip()[:26]:>26}{R}",
        f"  {GRAY}Expected CAGR             {R}{GREEN}{prof['mu']*100:>14.1f}%{R}",
        f"  {GRAY}Monte Carlo Success %     {R}{spc}{B}{sp:>13.1f}%{R}",
        f"  {GRAY}Inflation Rate Used       {R}{GRAY}{INFLATION*100:>14.1f}%{R}",
    ], "WEALTH SNAPSHOT", CYAN)
    print()

def show_insights(inc,exp,assets,goals,pname,prof,res,sp):
    rule("=",GOLD,"  AI INSIGHTS & RECOMMENDATIONS  ")
    print()

    def tip(icon,title,body,color=WHITE):
        words=body.split(); lines=[]; ln=""
        ml=W-10
        for w in words:
            if len(ln)+len(w)+1>ml: lines.append(f"  {color}{ln}{R}"); ln=w
            else: ln=(ln+" "+w).strip()
        if ln: lines.append(f"  {color}{ln}{R}")
        box(lines,f"{icon} {title}",GOLD); print()

    sr=res["sr"]
    if sr<10:
        tip("!","Low Savings Rate",
            f"Your {sr:.1f}% savings rate is critically below the 20%+ minimum. "
            "Audit entertainment, dining, and subscriptions first -- "
            "these offer the fastest cuts without major lifestyle impact.",RED)
    elif sr<20:
        tip("*","Improve Your Savings Rate",
            f"You save {sr:.1f}% annually. Pushing to 25% would significantly accelerate wealth. "
            "Set up an automatic transfer to investments on salary day.",GOLD)
    else:
        tip("+","Excellent Savings Discipline",
            f"Saving {sr:.1f}% is well above average. "
            "Compounding rewards patience -- stay consistent and avoid lifestyle inflation.",GREEN)

    if res["sip"]>res["mo_surplus"]:
        g2=res["sip"]-res["mo_surplus"]
        tip("!","SIP Funding Gap",
            f"Required SIP is {fmt(res['sip'])}/mo but your surplus is only "
            f"{fmt(res['mo_surplus'])}/mo (gap: {fmt(g2)}/mo). "
            f"Options: cut expenses by {fmt(g2*12)}/yr, extend retirement age 2-3 yrs, "
            "or boost income.",ORAN)
    else:
        tip("+","SIP is Achievable",
            f"Monthly surplus {fmt(res['mo_surplus'])} covers the required SIP of "
            f"{fmt(res['sip'])}. Set up a monthly auto-invest today!",GREEN)

    spc=GREEN if sp>=75 else GOLD if sp>=50 else RED
    if sp>=75:
        tip("+","High Success Probability",
            f"{sp:.0f}% of {MONTE_RUNS:,} simulations hit your target. "
            "Stay invested through downturns -- time in market beats timing the market.",GREEN)
    elif sp>=45:
        tip("*","Moderate Probability -- Act Now",
            f"{sp:.0f}% probability. Increase SIP by 10-15% annually (step-up SIP). "
            "Even small annual increases have dramatic compounding effects.",GOLD)
    else:
        tip("!","Low Success Probability",
            f"Only {sp:.0f}% probability. Four levers: (1) Increase SIP, "
            "(2) Extend timeline 3-5 yrs, (3) Switch to Aggressive profile, "
            "(4) Reduce target corpus. Combining all four dramatically boosts odds.",RED)

    ef=exp["total"]/12*6
    if assets["savings"]<ef:
        tip("$","Build Emergency Fund First",
            f"Maintain 6-month expenses ({fmt(ef)}) in liquid savings before investing. "
            f"Current savings: {fmt(assets['savings'])}. Without this buffer, downturns "
            "can force you to liquidate investments at a loss.",ORAN)

    if exp.get("loans",0)>inc["total"]*0.30:
        tip("!","High Debt Load",
            "Loan repayments exceed 30% of income. Prioritise clearing high-interest debt "
            "first -- it is a guaranteed return equal to the interest rate, "
            "often better than post-tax market returns.",RED)

    tip("i","Inflation Reality Check",
        f"At {INFLATION*100:.1f}% inflation, your current expenses of {fmt(exp['total'])} "
        f"will become {fmt(res['inf_exp'])} in {goals['years']} years. "
        f"Your corpus must support this future cost. "
        f"The {fmt(res['swr_mo'])}/mo sustainable draw is based on today's corpus value.",SKY)

# ─── MAIN ──────────────────────────────────────────────────────
def main():
    show_banner()
    box([
        f"  {SKY}Analyses your budget and uses AI market-trend simulations{R}",
        f"  {SKY}to forecast your financial future.{R}",
        f"  {GRAY}100% terminal output. No files. No internet.{R}",
    ],"About",CYAN)
    print()

    inc           = collect_income()
    exp           = collect_expenses()
    assets,goals  = collect_assets_goals()
    pname,prof    = choose_profile()

    rule("-",GRAY,"  Calculating...  ")
    res   = analyse(inc,exp,assets,goals,prof)
    paths = spinner("Running Monte Carlo simulation",
                    monte_carlo,inc,exp,assets,goals,prof)

    sp = (paths[:,-1]>=goals["target"]).mean()*100
    print()
    input(f"  {GOLD}Press Enter to view your results...{R} ")

    def section(title,fn,*args,**kwargs):
        fn(*args,**kwargs)
        input(f"\n  {GOLD}Press Enter to continue...{R} ")

    show_banner()
    show_summary_box(inc,exp,assets,goals,pname,prof,res,sp)
    section("budget",  show_budget_overview, inc,exp,res)
    section("projection", show_wealth_projection, inc,exp,assets,goals,prof,res)
    sp = section("monte", lambda: show_monte_carlo(paths,goals)) or sp
    # Re-run show_monte_carlo to capture return value
    show_monte_carlo(paths,goals)
    input(f"\n  {GOLD}Press Enter to continue...{R} ")
    section("profiles", show_profile_comparison, inc,exp,assets,goals)
    section("savings",  show_savings_meter, res)
    show_insights(inc,exp,assets,goals,pname,prof,res,sp)

    rule("=",GREEN,"  ANALYSIS COMPLETE  ")
    print(); center(f"{GOLD}{B}Thank you for using AI Wealth Visualiser. Invest wisely!{R}"); print()

    again=input(f"  {CYAN}>{R}  {WHITE}Run another analysis? (y/N){R}  {GOLD}:{R} ").strip().lower()
    if again=="y": main()

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {GRAY}Interrupted. Goodbye!{R}\n"); sys.exit(0)
