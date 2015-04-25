library(plm)

gfti = read.csv("../CDPdata/gfti.csv")

#################################
# effect of targets
#-------------------------------
ichi <- plm(lnintensity~hasintensity+Revenues+ROE, data=gfti, model="within")
icht <- plm(lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+Revenues+ROE, data=gfti, model="within")
ictlag <- plm(lnintensity~hasintensity+hasabsolute+hasintensity*hasabsolute+lag(hasintensity,1)+lag(hasabsolute,1)+lag(hasintensity*hasabsolute,1)+Revenues+ROE, data=gfti, model="within")
icha <- plm(lnintensity~hasabsolute, data=gfti, model="within")
# sector specific effects of intensity target
icshasint2 <- plm(lnintensity~Sector:hasintensity,data=gfti, model="within")

#################################
# effect of savings
#-------------------------------
icssave <- plm(lnintensity~pCOGS + pPPE, data=gfti, model="within")
icssave2 <- plm(lnintensity~pCOGS+pPPE+pCOGS*pPPE+ROE, data=gfti, model="within")


#################################
# interactive effect of targets and savings
#-------------------------------
icsts <- plm(lnintensity~pCOGS+pPPE+pCOGS*hasintensity+pCOGS*hasabsolute+pPPE*hasintensity+pPPE*hasabsolute+ROE, data=gfti, model="within")
icsts2 <- plm(lnintensity~pCOGS+pPPE+pCOGS*pPPE+ROE+pCOGS*hasintensity+pCOGS*hasabsolute+pPPE*hasintensity+pPPE*hasabsolute+pCOGS*pPPE*hasintensity+pCOGS*pPPE*hasabsolute+pCOGS*pPPE*hasintensity*hasabsolute, data=gfti, model="within")


################################
# lag
#-------------------------------
# effect of last year
# negative means that lower intensity last year leads to increase in current year
ily1 <- plm(lnintensity~lag(lnintensity, 1), data=gfti, model="within")
# effect broken out by sector, no longer significant
ily1sector <- plm(lnintensity~Sector:lag(lnintensity, 1), data=gfti, model="pooling")

# positive means that lower intensity in previous year leads to lower in current year
ily2 <- plm(lnintensity~lag(lnintensity,1)+lag(lnintensity,2), data=gfti, model="pooling")

ily3 <- plm(lnintensity~lag(lnintensity,1)+lag(lnintensity,2)+lag(lnintensity,3), data=gfti, model="pooling")
