library(plm)

gfti = read.csv("../CDPdata/gfti.csv")
p2 = read.csv("../CDPdata/profiles2.csv")
pls = read.csv("../CDPdata/plateaus.csv")
sts = read.csv("../CDPdata/steadys.csv")
us = read.csv("../CDPdata/us.csv")
notus = read.csv("../CDPdata/notus.csv")
uk = read.csv("../CDPdata/uk.csv")
safrica = read.csv("../CDPdata/safrica.csv")
france = read.csv("../CDPdata/france.csv")
germany = read.csv("../CDPdata/germany.csv")
japan = read.csv("../CDPdata/japan.csv")

## sector data
ind = read.csv("../CDPdata/Industrials.csv")
mat = read.csv("../CDPdata/Materials.csv")
cd = read.csv("../CDPdata/ConsumerDiscretionary.csv")
cs = read.csv("../CDPdata/ConsumerStaples.csv")
it = read.csv("../CDPdata/InformationTechnology.csv")
ut = read.csv("../CDPdata/Utilities.csv")
en = read.csv("../CDPdata/Energy.csv")

#################################
# sectors
#--------------------------------

sectars <- lnintensity~(hasintensity+hasabsolute)*(Industrials+ConsumerDiscretionary+Materials+InformationTechnology+ConsumerStaples+Utilities+Energy)+Revenues
p2.sectars <- plm(sectars, data=p2, model="within")

secsavs <- lnintensity~(pCOGS+pPPE)*(Industrials+ConsumerDiscretionary+Materials+InformationTechnology+ConsumerStaples+Utilities+Energy)+Revenues
p2.secsavs <- plm(secsavs, data=p2, model="within")

secsavs2 <- lnintensity~(pCOGS+pPPE+pCOGS*pPPE)*(Industrials+ConsumerDiscretionary+Materials+InformationTechnology+ConsumerStaples+Utilities+Energy)+Revenues
p2.secsavs2 <- plm(secsavs2, data=p2, model="within")


secsavs3 <- lnintensity~(lnCOGS+lnPPE+lnCOGS*lnPPE)*(Industrials+ConsumerDiscretionary+Materials+InformationTechnology+ConsumerStaples+Utilities+Energy)+Revenues
p2.secsavs3 <- plm(secsavs3, data=p2, model="within")

secsavs4 <- lnintensity~(lnCOGS+lnPPE)*(Industrials+ConsumerDiscretionary+Materials+InformationTechnology+ConsumerStaples+Utilities+Energy)+Revenues
p2.secsavs4 <- plm(secsavs4, data=p2, model="within")

#################################
# countries
#--------------------------------
cntrars <- lnintensity~(hasintensity+hasabsolute)*(USA+UnitedKingdom+Japan+SouthAfrica+France+SouthKorea+Germany)+Revenues
p2.cntrars <- plm(cntrars, data=p2, model="within")

cntrars2 <- lnintensity~(hasintensity+hasabsolute+hasintensity*hasabsolute)*(USA+UnitedKingdom+Japan+SouthAfrica+France+SouthKorea+Germany)+Revenues
p2.cntrars2 <- plm(cntrars2, data=p2, model="within")

cntsavs <- lnintensity~(pCOGS+pPPE)*(USA+UnitedKingdom+Japan+SouthAfrica+France+SouthKorea+Germany)+Revenues
p2.cntsavs <- plm(cntsavs, data=p2, model="within")

cntsavs2 <- lnintensity~(pCOGS+pPPE+pCOGS*pPPE)*(USA+UnitedKingdom+Japan+SouthAfrica+France+SouthKorea+Germany)+Revenues
p2.cntsavs2 <- plm(cntsavs2, data=p2, model="within")


cntsavs3 <- lnintensity~(lnCOGS+lnPPE+lnCOGS*lnPPE)*(USA+UnitedKingdom+Japan+SouthAfrica+France+SouthKorea+Germany)+Revenues
p2.cntsavs3 <- plm(cntsavs3, data=p2, model="within")


cntarsavs <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE)*(USA+UnitedKingdom+Japan+SouthAfrica+France+SouthKorea+Germany)+Revenues
p2.cntarsavs <- plm(cntarsavs, data=p2, model="within")

cntarsavs2 <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE+pCOGS*pPPE)*(USA+UnitedKingdom+Japan+SouthAfrica+France+SouthKorea+Germany)+Revenues
p2.cntarsavs2 <- plm(cntarsavs2, data=p2, model="within")

#################################
# effect of targets
#-------------------------------

tform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+Revenues+ROE
gfti.t <- plm(tform, data=gfti, model="within")
pls.t <- plm(tform,data=pls, model="within")
sts.t <- plm(tform,data=sts, model="within")
us.t <- plm(tform, data=us, model="within")

tcform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+factor(country)+Revenues+ROE
p2.tc <- plm(tcform, data=p2, model="within")

tpform <- lnintensity~hasintensity+hasintensity*plateau+hasintensity*steady+hasabsolute*plateau+hasabsolute*steady+hasintensity*hasabsolute+hasintensity*hasabsolute*plateau+hasintensity*hasabsolute*steady+ROE+Revenues
p2.tp <- plm(tpform, data=p2, effect="twoways", model="within")

tp2form <- lnintensity~hasintensity+hasintensity*plateau+hasintensity*steady+hasabsolute*plateau+hasabsolute*steady+Revenues+ROE
p2.tp2 <- plm(tp2form, data=p2, effect="twoways", model="within")

tlagform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+lag(hasintensity,1)+lag(hasabsolute,1)+lag(hasintensity*hasabsolute,1)+Revenues+ROE
gfti.tlags <- plm(tlagform, data=gfti, effect="twoways", model="within")

# sector specific effects of intensity target
# icshasint2 <- plm(lnintensity~Sector:hasintensity,data=gfti, model="within")

#################################
# effect of savings
#-------------------------------
# icssave <- plm(lnintensity~pCOGS + pPPE+Revenues, data=gfti, model="within")

sform <- lnintensity~pCOGS+pPPE+pCOGS*pPPE+Revenues+ROE
gfti.s <- plm(sform, data=gfti, effect="twoways", model="within")
pls.s <- plm(sform,data=pls, model="within")
sts.s <- plm(sform,data=sts, model="within")
us.s <- plm(sform,data=sts, model="within")

scform <- lnintensity~pCOGS+pPPE+pCOGS*pPPE+factor(country)+Revenues+ROE
p2.sc <- plm(scform, data=p2, model="within")

spform <- lnintensity~pCOGS+pCOGS*plateau+pCOGS*steady+pPPE+pPPE*plateau+pPPE*steady+pCOGS*pPPE+pCOGS*pPPE*plateau+pCOGS*pPPE*steady+Revenues+ROE
p2.sp <- plm(spform, data=p2, model="within")



lnsform <- lnintensity~lnCOGS+lnPPE+lnCOGS*lnPPE+Revenues+ROE
lns2form <- lnintensity~lnCOGS+lnPPE+Revenues+ROE
p2.lns <- plm(lnsform,data=p2, model="within")
us.lns <- plm(lnsform,data=us, model="within")

lnscform <- lnintensity~lnCOGS+lnPPE+lnCOGS*lnPPE+factor(country)+Revenues+ROE
lnsc2form <- lnintensity~lnCOGS+lnPPE+factor(country)+Revenues+ROE
p2.lnsc <- plm(lnscform,data=p2, model="within")



#################################
# interactive effect of targets and savings
#-------------------------------
# pCOGS and pPPE interact with targets separately
iform <- lnintensity~ (hasintensity+hasabsolute)*(pCOGS+pPPE)+ROE + Revenues
gfti.i <- plm(iform, data=gfti, model="within")
pls.i <- plm(iform,data=pls, model="within")
sts.i <- plm(iform,data=sts, model="within")

# pCOGS and pPPE interact with targets separately and with profiles
ipform <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE)*(plateau+steady)+ROE+Revenues
p2.ip <- plm(ipform, data=p2, model="within")


# pCOGS and pPPE interact with each other and with targets.
iiform <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE+pCOGS*pPPE)+Revenues+ROE
gfti.ii <- plm(iiform,data=gfti, model="within")

iicform <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE+pCOGS*pPPE)+factor(country)+Revenues+ROE
p2.iic <- plm(iicform, data=p2, model="within")


lniiform <- lnintensity~(hasintensity+hasabsolute)*(lnCOGS+lnPPE+lnCOGS*lnPPE)+Revenues+ROE
p2.lnii <- plm(lniiform,data=p2, model="within")

lniicform <- lnintensity~(hasintensity+hasabsolute)*(lnCOGS+lnPPE+lnCOGS*lnPPE)+factor(country)+Revenues+ROE
p2.lniic <- plm(lniicform, data=p2, model="within")



# pCOGS and pPPE interact with each other and with targets and with profiles.  targets don't interact
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
