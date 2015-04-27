library(plm)

gfti = read.csv("../CDPdata/gfti.csv")
p2 = read.csv("../CDPdata/profiles2.csv")

#################################
# effect of targets
#-------------------------------

tform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+Revenues
gfti.t <- plm(tform, data=gfti, model="within")

tpform <- lnintensity~hasintensity+hasintensity*plateau+hasintensity*steady+hasabsolute*plateau+hasabsolute*steady+hasintensity*hasabsolute+hasintensity*hasabsolute*plateau+hasintensity*hasabsolute*steady+Revenues
p2.tp <- plm(tpform, data=p2, model="within")

tp2form <- lnintensity~hasintensity+hasintensity*plateau+hasintensity*steady+hasabsolute*plateau+hasabsolute*steady+Revenues
p2.tp2 <- plm(tp2form, data=p2, model="within")

tlagform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+lag(hasintensity,1)+lag(hasabsolute,1)+lag(hasintensity*hasabsolute,1)+Revenues
gfti.tlags <- plm(tlagform, data=gfti, model="within")

# sector specific effects of intensity target
# icshasint2 <- plm(lnintensity~Sector:hasintensity,data=gfti, model="within")

#################################
# effect of savings
#-------------------------------
# icssave <- plm(lnintensity~pCOGS + pPPE+Revenues, data=gfti, model="within")

sform <- lnintensity~pCOGS+pPPE+pCOGS*pPPE+Revenues+ROE
gfti.s <- plm(sform, data=gfti, model="within")

spform <- lnintensity~pCOGS+pCOGS*plateau+pCOGS*steady+pPPE+pPPE*plateau+pPPE*steady+pCOGS*pPPE+pCOGS*pPPE*plateau+pCOGS*pPPE*steady+Revenues+ROE
p2.sp <- plm(spform, data=p2, model="within")

#################################
# interactive effect of targets and savings
#-------------------------------
# pCOGS and pPPE interact with targets separately
iform <- lnintensity~hasintensity+hasabsolute+pCOGS+pPPE+pCOGS*hasintensity+pCOGS*hasabsolute+pPPE*hasintensity+pPPE*hasabsolute+ROE+Revenues
gfti.i <- plm(iform, data=gfti, model="within")

# pCOGS and pPPE interact with targets separately and with profiles
ipform <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE)*(plateau+steady)+ROE+Revenues
p2.ip <- plm(ipform, data=p2, model="within")

# pCOGS and pPPE interact with each other and with targets.  targets don't interact
iipform <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE+pCOGS*pPPE)*(plateau+steady)+Revenues+ROE
p2.ii <- plm(iipform, data=p2, model="within")

################################
# lag
#-------------------------------
# effect of last year
# negative means that lower intensity last year leads to increase in current year
# ily1 <- plm(lnintensity~lag(lnintensity, 1), data=gfti, model="within")
# effect broken out by sector, no longer significant
# ily1sector <- plm(lnintensity~Sector:lag(lnintensity, 1), data=gfti, model="pooling")

# positive means that lower intensity in previous year leads to lower in current year
# ily2 <- plm(lnintensity~lag(lnintensity,1)+lag(lnintensity,2), data=gfti, model="pooling")

# ily3 <- plm(lnintensity~lag(lnintensity,1)+lag(lnintensity,2)+lag(lnintensity,3), data=gfti, model="pooling")
