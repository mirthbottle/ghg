library(plm)

# gfti = read.csv("../CDPdata/gfti.csv")
p2 = read.csv("../CDPdata/profiles2.csv")
pls = read.csv("../CDPdata/plateaus.csv")
sts = read.csv("../CDPdata/steadys.csv")
notplst = read.csv("../CDPdata/notplst.csv")

us = read.csv("../CDPdata/us.csv")
notus = read.csv("../CDPdata/notus.csv")
uk = read.csv("../CDPdata/uk.csv")
safrica = read.csv("../CDPdata/safrica.csv")
france = read.csv("../CDPdata/france.csv")
germany = read.csv("../CDPdata/germany.csv")
japan = read.csv("../CDPdata/japan.csv")
skorea = read.csv("../CDPdata/skorea.csv")

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
ind.t <- plm(tform, data=ind, model="within")
mat.t <- plm(tform, data=mat, model="within")
cd.t <- plm(tform, data=cd, model="within")
cs.t <- plm(tform, data=cs, model="within")
it.t <- plm(tform, data=it, model="within")
ut.t <- plm(tform, data=ut, model="within")
en.t <- plm(tform, data=en, model="within")


ind.s <- plm(sform, data=ind, model="within")
mat.s <- plm(sform, data=mat, model="within")
cd.s <- plm(sform, data=cd, model="within")
cs.s <- plm(sform, data=cs, model="within")
it.s <- plm(sform, data=it, model="within")
ut.s <- plm(sform, data=ut, model="within")
en.s <- plm(sform, data=en, model="within")


ind.lns <- plm(lnsform, data=ind, model="within")
mat.lns <- plm(lnsform, data=mat, model="within")
cd.lns <- plm(lnsform, data=cd, model="within")
cs.lns <- plm(lnsform, data=cs, model="within")
it.lns <- plm(lnsform, data=it, model="within")
ut.lns <- plm(lnsform, data=ut, model="within")
en.lns <- plm(lnsform, data=en, model="within")

#################################
# countries
#--------------------------------
us.t <- plm(tform, data=us, model="within")
notus.t <- plm(tform, data=notus, model="within")
uk.t <- plm(tform, data=uk, model="within")
safrica.t <- plm(tform, data=safrica, model="within")
france.t <- plm(tform, data=france, model="within")
germany.t <- plm(tform, data=germany, model="within")
japan.t <- plm(tform, data=japan, model="within")
skorea.t <- plm(tform, data=skorea, model="within")

us.s <- plm(sform,data=sts, model="within")
notus.s <- plm(sform, data=notus, model="within")
uk.s <- plm(sform, data=uk, model="within")
safrica.s <- plm(sform, data=safrica, model="within")
france.s <- plm(sform, data=france, model="within")
germany.s <- plm(sform, data=germany, model="within")
japan.s <- plm(sform, data=japan, model="within")
skorea.s <- plm(sform, data=skorea, model="within")

us.lns <- plm(lnsform,data=us, model="within")
notus.lns <- plm(lnsform, data=notus, model="within")
uk.lns <- plm(lnsform, data=uk, model="within")
safrica.lns <- plm(lnsform, data=safrica, model="within")
france.lns <- plm(lnsform, data=france, model="within")
germany.lns <- plm(lnsform, data=germany, model="within")
japan.lns <- plm(lnsform, data=japan, model="within")
skorea.lns <- plm(lnsform, data=skorea, model="within")

#################################
# effect of targets
#-------------------------------

tform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+Revenues+ROE
p2.t <- plm(tform, data=p2, model="within")
pls.t <- plm(tform,data=pls, model="within")
sts.t <- plm(tform,data=sts, model="within")
notplst.t <- plm(tform,data=notplst, model="within")

tcform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+factor(country)+Revenues+ROE
# p2.tc <- plm(tcform, data=p2, model="within")

tpform <- lnintensity~(hasintensity+hasabsolute+hasintensity*hasabsolute)*(plateau+steady)+ROE+Revenues
p2.tp <- plm(tpform, data=p2, model="within")

tlagform <- lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+lag(hasintensity,1)+lag(hasabsolute,1)+lag(hasintensity*hasabsolute,1)+Revenues+ROE


#################################
# effect of savings
#-------------------------------
# icssave <- plm(lnintensity~pCOGS + pPPE+Revenues, data=gfti, model="within")

sform <- lnintensity~pCOGS+pPPE+pCOGS*pPPE+Revenues+ROE
p2.s <- plm(sform, data=p2, model="within")
pls.s <- plm(sform,data=pls, model="within")
sts.s <- plm(sform,data=sts, model="within")
notplst.s <- plm(sform,data=notplst, model="within")

spform <- lnintensity~pCOGS+pCOGS*plateau+pCOGS*steady+pPPE+pPPE*plateau+pPPE*steady+pCOGS*pPPE+pCOGS*pPPE*plateau+pCOGS*pPPE*steady+Revenues+ROE
p2.sp <- plm(spform, data=p2, model="within")


lnsform <- lnintensity~lnCOGS+lnPPE+lnCOGS*lnPPE+Revenues+ROE
lns2form <- lnintensity~lnCOGS+lnPPE+Revenues+ROE
p2.lns <- plm(lnsform,data=p2, model="within")
pls.lns <- plm(lnsform,data=pls, model="within")
sts.lns <- plm(lnsform,data=sts, model="within")
notplst.lns <- plm(lnsform,data=notplst, model="within")

#################################
# interactive effect of targets and savings
#-------------------------------
# pCOGS and pPPE interact with targets separately
iform <- lnintensity~ (hasintensity+hasabsolute)*(pCOGS+pPPE)+ROE + Revenues
p2.i <- plm(iform, data=p2, model="within")

# pCOGS and pPPE interact with targets separately and with profiles
ipform <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE)*(plateau+steady)+ROE+Revenues
p2.ip <- plm(ipform, data=p2, model="within")


# pCOGS and pPPE interact with each other and with targets.
iiform <- lnintensity~(hasintensity+hasabsolute)*(pCOGS+pPPE+pCOGS*pPPE)+Revenues+ROE
p2.ii <- plm(iiform,data=p2, model="within")
pls.ii <- plm(iiform,data=pls, model="within")
sts.ii <- plm(iiform,data=sts, model="within")
notplst.ii <- plm(iiform,data=notplst, model="within")

lniiform <- lnintensity~(hasintensity+hasabsolute)*(lnCOGS+lnPPE+lnCOGS*lnPPE)+Revenues+ROE
p2.lnii <- plm(lniiform,data=p2, model="within")
pls.lnii <- plm(lniiform,data=pls, model="within")
sts.lnii <- plm(lniiform,data=sts, model="within")
notplst.lnii <- plm(lniiform,data=notplst, model="within")

lniicform <- lnintensity~(hasintensity+hasabsolute)*(lnCOGS+lnPPE+lnCOGS*lnPPE)+factor(country)+Revenues+ROE
# p2.lniic <- plm(lniicform, data=p2, model="within")



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
