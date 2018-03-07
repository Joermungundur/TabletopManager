'''
Created on 29.11.2017

http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
@author: mabelli
'''
from Database.Tables import t_Color, t_Company, t_System, t_Setting, zt_System_Setting, \
    t_Color_Type, t_Brush_Type, t_Brush
from Database.Colors import createWPColors


def create_database(session):
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

    ct_ABP = t_Color_Type(Name="Acrylic base paint",
                          Description="A standard color for appliance by brush")
    ct_AAP = t_Color_Type(Name="Acrylic airbrush paint",
                          Description="A finer pigmented color that can be applied by brush or airbrush")
    ct_AEP = t_Color_Type(Name="Acrylic effect paint",
                          Description="A color that achieves a certain effect, for example gloss")
    ct_AWa = t_Color_Type(Name="Acrylic Wash",
                          Description="A very much watered down color used for 'washing'")
    ct_Var = t_Color_Type(Name="Varnish",
                          Description="A Varnish protects a miniature")
    ct_Pri = t_Color_Type(Name="Primer",
                          Description="Used to improve adhesiveness of following color layers")
    ct_Uti = t_Color_Type(Name="Utility",
                          Description="Generic category")
    colorTypes = [ct_ABP, ct_AAP, ct_AEP, ct_AWa, ct_Var, ct_Pri, ct_Uti]
    session.add_all(colorTypes)
    session.commit()

    bt_DB = t_Brush_Type(Name="Detail Brush",
                         Description="A very small brush for very small details")
    bt_SB = t_Brush_Type(Name="Standard Brush",
                         Description="A standard brush used for the bulk of the painting")
    bt_BB = t_Brush_Type(Name="Drybrush",
                         Description="A brush used for highlighting details by drybrushing them")
    bt_TB = t_Brush_Type(Name="Tan Brush",
                         Description="A big brush for basecoating tanks or monsters")
    brushTypes = [bt_DB, bt_SB, bt_BB, bt_TB]
    session.add_all(brushTypes)
    session.commit()

    createWPColors(t_Color, session, co_AP.ID, colorTypes)
    session.add_all([sy_W4, sy_DF, sy_DZ,
                     se_SF, se_MB, se_FB, se_DY])
    session.commit()

    br_TP = t_Brush(Name="The Psycho",
                    Description="The first of its kind made specifically for Wargaming, the Psycho is aptly named as "
                                "it is indeed very small and ultra precise for that perfect lining or miniscule "
                                "detail. Handmade from first-class Rothmarder Sable and with the elegant and famous "
                                "triangular handle - this brush is sure to become a hit with painters wanting nothing "
                                "less than nano-precision.",
                    C_ID=co_AP.ID,
                    BT_ID=bt_DB.ID)
    br_DE = t_Brush(Name="Detail",
                    Description="This superb sable brush allows you make very precise details on your models, "
                                "be they weapon cartridges or very fine highlights on a face.",
                    C_ID=co_AP.ID,
                    BT_ID=bt_DB.ID)
    br_RE = t_Brush(Name="Regiment",
                    Description="The Rotmarder sable hairs on this brush and its considerable size makes the Regiment "
                                "brush spectacular for speedpainting big swathes of troops. The sharp tip makes "
                                "basecoating with this brush really easy and fast.",
                    C_ID=co_AP.ID,
                    BT_ID=bt_SB.ID)
    br_SD = t_Brush(Name="Small Drybrush",
                    Description="This is a very popular brush and as its bigger brother, this spectacular drybrush "
                                "has a 43 degree angle cut to make it no less than perfect for drybrushing small "
                                "miniatures. The size of this brush is designed for drybrushing areas of a model, "
                                "like chainmail or a weapon - and not neccessarily the whole model at once. ",
                    C_ID=co_AP.ID,
                    BT_ID=bt_DB.ID)
    br_LD = t_Brush(Name="Large Drybrush",
                    Description="This speciality drybrush has a 43 degree angle cut on the hard tip, making it "
                                "absolutely unique in design and superb for drybrushing - as you will not have to "
                                "bend your wrist to hit the model 100% due to the expert cut. This Brush is a must "
                                "have for the serious painter!",
                    C_ID=co_AP.ID,
                    BT_ID=bt_DB.ID)
    br_VS = t_Brush(Name="Vehicle & Scenery",
                    Description="The Vehicle brush has a flat stiff end making it perfect for highligting edges on "
                                "tanks and drybrushing anything from scenery to most vehicles. Also large monsters "
                                "benefit from this brush where it is used as an enormous drybrush.",
                    C_ID=co_AP.ID,
                    BT_ID=bt_TB.ID)
    brushes = [br_TP, br_DE, br_RE, br_SD, br_LD, br_VS]
    session.add_all(brushes)
    session.commit()

    zss_W4_SF = zt_System_Setting(Sy_ID=sy_W4.ID,
                                  Se_ID=se_SF.ID)
    zss_W4_MB = zt_System_Setting(Sy_ID=sy_W4.ID,
                                  Se_ID=se_MB.ID)
    zss_W4_DY = zt_System_Setting(Sy_ID=sy_W4.ID,
                                  Se_ID=se_DY.ID)
    zss_DF_SF = zt_System_Setting(Sy_ID=sy_DF.ID,
                                  Se_ID=se_SF.ID)
    zss_DF_FB = zt_System_Setting(Sy_ID=sy_DF.ID,
                                  Se_ID=se_FB.ID)
    zss_DZ_SF = zt_System_Setting(Sy_ID=sy_DZ.ID,
                                  Se_ID=se_SF.ID)
    zss_DZ_MB = zt_System_Setting(Sy_ID=sy_DZ.ID,
                                  Se_ID=se_MB.ID)

    session.add_all([zss_W4_SF, zss_W4_MB, zss_W4_DY,
                     zss_DF_SF, zss_DF_FB,
                     zss_DZ_SF, zss_DZ_MB])
    session.commit()
