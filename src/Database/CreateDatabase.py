'''
Created on 29.11.2017

http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
@author: mabelli
'''
from Database.Tables import t_Color, t_Company, t_System, t_Setting, zt_System_Setting
from Database.Colors import createWPColors
 
def createDatabase(session):
    
    co_GW = t_Company(Name="Games Workshop",
                        Description="Der Platzhirsch",
                        Website="www.gamesworkshop.de")
    co_MG = t_Company(Name="Mantic Games",
                        Description="Der Newcomer",
                        Website="www.mantic-games.com")
    co_AP = t_Company(Name="The Army Painter",
                        Description="Colors and hobby tools",
                        Website="www.thearmypainter.com")
    co_HW = t_Company(Name="Hawk Wargames",
                        Description="Cool SciFi games",
                        Website="www.hawkwargames.com")
    
    session.add_all([co_GW, co_MG, co_AP, co_HW])
    session.commit()
    
    sy_W4 = t_System(C_ID=co_GW.ID,
                       Name="Warhammer 40.000",
                       Description="Dark Future SciFi Mass Battle")
    sy_DF = t_System(C_ID=co_HW.ID,
                       Name="Dropfleet Commander",
                       Description="SciFi Fleet Battle")
    sy_DZ = t_System(C_ID=co_HW.ID,
                       Name="Dropzone Commander",
                       Description="10mm SciFi Mass Battle")
    
    se_SF = t_Setting(Name="SciFi",
                        Description="A system set in the future with considerable " + 
                                    "scientific advances")
    se_MB = t_Setting(Name="Mass Battle System",
                        Description="A system that uses great numbers of miniatures")
    se_FB = t_Setting(Name="Fleet based battle game",
                        Description="A system that works not with ground based armies " + 
                                    "but either water or space based fleets")
    se_DY = t_Setting(Name="Dystopia",
                        Description="A system set in universe where things didn't " + 
                                    "necessarily for the best")
    
    createWPColors(t_Color, session, co_AP.ID)
    
    session.add_all([sy_W4, sy_DF, sy_DZ,
                     se_SF, se_MB, se_FB, se_DY]) 
    session.commit()
    
    zss_W4_SF = zt_System_Setting(Sy_ID = sy_W4.ID,
                                  Se_ID = se_SF.ID)
    zss_W4_MB = zt_System_Setting(Sy_ID = sy_W4.ID,
                                  Se_ID = se_MB.ID)
    zss_W4_DY = zt_System_Setting(Sy_ID = sy_W4.ID,
                                  Se_ID = se_DY.ID)
    zss_DF_SF = zt_System_Setting(Sy_ID = sy_DF.ID,
                                  Se_ID = se_SF.ID)
    zss_DF_FB = zt_System_Setting(Sy_ID = sy_DF.ID,
                                  Se_ID = se_FB.ID)
    zss_DZ_SF = zt_System_Setting(Sy_ID = sy_DZ.ID,
                                  Se_ID = se_SF.ID)
    zss_DZ_MB = zt_System_Setting(Sy_ID = sy_DZ.ID,
                                  Se_ID = se_MB.ID)
    
    session.add_all([zss_W4_SF, zss_W4_MB, zss_W4_DY,
                     zss_DF_SF, zss_DF_FB,
                     zss_DZ_SF, zss_DZ_MB])
    session.commit() 