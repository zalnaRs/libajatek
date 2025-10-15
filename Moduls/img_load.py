from pygame import image

#Kezdőlap képei

background_img = image.load("Assets/Hatter/hatter.png").convert_alpha()
start_background_img = image.load("Assets/Hatter/hatterkep.png").convert_alpha()

resume_img = image.load("Assets/Gombok/folytat_gomb.png").convert_alpha()
resume_le = image.load("Assets/Gombok/folytat_gomb_le.png").convert_alpha()
quit_img = image.load("Assets/Gombok/quit_gomb.png").convert_alpha()
quit_le = image.load("Assets/Gombok/quit_gomb_le.png").convert_alpha()
start_img = image.load("Assets/Gombok/kezd_gomb.png").convert_alpha()
start_le = image.load("Assets/Gombok/kezd_gomb_le.png").convert_alpha()
back_img = image.load("Assets/Gombok/vissza_gomb.png").convert_alpha()
back_le = image.load("Assets/Gombok/vissza_gomb_le.png").convert_alpha()
lvl1_img = image.load("Assets/Gombok/1_gomb.png").convert_alpha()
lvl1_le = image.load("Assets/Gombok/1_gomb_le.png").convert_alpha()
lvl2_img = image.load("Assets/Gombok/2_gomb.png").convert_alpha()
lvl2_le = image.load("Assets/Gombok/2_gomb_le.png").convert_alpha()
lvl3_img = image.load("Assets/Gombok/3_gomb.png").convert_alpha()
lvl3_le = image.load("Assets/Gombok/3_gomb_le.png").convert_alpha()
lvl4_img = image.load("Assets/Gombok/4_gomb.png").convert_alpha()
lvl4_le = image.load("Assets/Gombok/4_gomb_le.png").convert_alpha()
left_img = image.load("Assets/Gombok/balra.png").convert_alpha()
left_kijelolve = image.load("Assets/Gombok/balra_kijelolve.png").convert_alpha()
right_img = image.load("Assets/Gombok/jobbra.png").convert_alpha()
right_kijelolve = image.load("Assets/Gombok/jobbra_kijelolve.png").convert_alpha()

#   --Bomba és elemeinek képei--

bomb_img = image.load("Assets/Hatter/bomba_alap.png").convert_alpha()

#Sima drótok modul elmei

sim_drot_modul_img = image.load("Assets/modul_drotok/sima_drotok_224x224.png").convert_alpha()

fekete_drot_img = image.load("Assets/modul_drotok/fekete/fekete_alap.png").convert_alpha()
fekete_drot_action = (image.load("Assets/modul_drotok/fekete/fekete_kijelolve.png").convert_alpha(), image.load("Assets/modul_drotok/fekete/fekete_vagas.png").convert_alpha(), image.load("Assets/modul_drotok/fekete/fekete_kesz.png").convert_alpha())
kek_drot_img = image.load("Assets/modul_drotok/kek/kek_alap.png").convert_alpha()
kek_drot_action = (image.load("Assets/modul_drotok/kek/kek_kijelolve.png").convert_alpha(), image.load("Assets/modul_drotok/kek/kek_vagas.png").convert_alpha(), image.load("Assets/modul_drotok/kek/kek_kesz.png").convert_alpha())
piros_drot_img = image.load("Assets/modul_drotok/piros/piros_alap.png").convert_alpha()
piros_drot_action = (image.load("Assets/modul_drotok/piros/piros_kijelolve.png").convert_alpha(), image.load("Assets/modul_drotok/piros/piros_vagas.png").convert_alpha(), image.load("Assets/modul_drotok/piros/piros_kesz.png").convert_alpha())
sarga_drot_img = image.load("Assets/modul_drotok/sarga/sarga_alap.png").convert_alpha()
sarga_drot_action = (image.load("Assets/modul_drotok/sarga/sarga_kijelolve.png").convert_alpha(), image.load("Assets/modul_drotok/sarga/sarga_vagas.png").convert_alpha(), image.load("Assets/modul_drotok/sarga/sarga_kesz.png").convert_alpha())

#Komplex kábelek modul elmei

kom_kabel_modul_img = image.load("Assets/modul_kabel/komplex_kabelek_224x224.png").convert_alpha()

kabel_1_img = image.load("Assets/modul_kabel/1_kabel/1_alap.png").convert_alpha()
kabel_1_action = (image.load("Assets/modul_kabel/1_kabel/1_kijelolve.png").convert_alpha(), image.load("Assets/modul_kabel/1_kabel/1_vagas.png").convert_alpha(), image.load("Assets/modul_kabel/1_kabel/1_kesz.png").convert_alpha())
kabel_2_img = image.load("Assets/modul_kabel/2_kabel/2_alap.png").convert_alpha()
kabel_2_action = (image.load("Assets/modul_kabel/2_kabel/2_kijelolve.png").convert_alpha(), image.load("Assets/modul_kabel/2_kabel/2_vagas.png").convert_alpha(), image.load("Assets/modul_kabel/2_kabel/2_kesz.png").convert_alpha())
kabel_3_img = image.load("Assets/modul_kabel/3_kabel/3_alap.png").convert_alpha()
kabel_3_action = (image.load("Assets/modul_kabel/3_kabel/3_kijelolve.png").convert_alpha(), image.load("Assets/modul_kabel/3_kabel/3_vagas.png").convert_alpha(), image.load("Assets/modul_kabel/3_kabel/3_kesz.png").convert_alpha())
kabel_4_img = image.load("Assets/modul_kabel/4_kabel/4_alap.png").convert_alpha()
kabel_4_action = (image.load("Assets/modul_kabel/4_kabel/4_kijelolve.png").convert_alpha(), image.load("Assets/modul_kabel/4_kabel/4_vagas.png").convert_alpha(), image.load("Assets/modul_kabel/4_kabel/4_kesz.png").convert_alpha())

#Gomb modul elmei

gomb_modul_img = image.load("Assets/modul_gomb/gomb_224x224.png").convert_alpha()

kek_gomb_img = image.load("Assets/modul_gomb/kek/kek_sima.png").convert_alpha()
kek_gomb_action = (image.load("Assets/modul_gomb/kek/kek_kijelol.png").convert_alpha(), image.load("Assets/modul_gomb/kek/kek_benyomva.png").convert_alpha(), image.load("Assets/modul_gomb/kek/kek_kesz.png").convert_alpha())
piros_gomb_img = image.load("Assets/modul_gomb/piros/piros_sima.png").convert_alpha()
piros_gomb_action = (image.load("Assets/modul_gomb/piros/piros_kijelol.png").convert_alpha(), image.load("Assets/modul_gomb/piros/piros_benyomva.png").convert_alpha(), image.load("Assets/modul_gomb/piros/piros_kesz.png").convert_alpha())
zold_gomb_img = image.load("Assets/modul_gomb/zold/zold_sima.png").convert_alpha()
zold_gomb_action = (image.load("Assets/modul_gomb/zold/zold_kijelol.png").convert_alpha(), image.load("Assets/modul_gomb/zold/zold_benyomva.png").convert_alpha(), image.load("Assets/modul_gomb/zold/zold_kesz.png").convert_alpha())

lud_szimbolum = image.load("Assets/modul_gomb/szimbolumok/minta_lud.png").convert_alpha()
talp_szimbolum = image.load("Assets/modul_gomb/szimbolumok/minta_talp.png").convert_alpha()
tojas_szimbolum = image.load("Assets/modul_gomb/szimbolumok/minta_tojas.png").convert_alpha()

#Kérdések modul elmei

kerdes_modul_img = image.load("Assets/modul_kerdesek/kerdesek_panel_224x224.png").convert_alpha()

a_gomb_img = image.load("Assets/modul_kerdesek/A/a_alap.png").convert_alpha()
a_gomb_action = (image.load("Assets/modul_kerdesek/A/a_kijelol.png").convert_alpha(), image.load("Assets/modul_kerdesek/A/a_benyom.png").convert_alpha())
b_gomb_img = image.load("Assets/modul_kerdesek/B/b_alap.png").convert_alpha()
b_gomb_action = (image.load("Assets/modul_kerdesek/B/b_kijelol.png").convert_alpha(), image.load("Assets/modul_kerdesek/B/b_benyom.png").convert_alpha())
c_gomb_img = image.load("Assets/modul_kerdesek/C/c_alap.png").convert_alpha()
c_gomb_action = (image.load("Assets/modul_kerdesek/C/c_kijelol.png").convert_alpha(), image.load("Assets/modul_kerdesek/C/c_benyom.png").convert_alpha())
d_gomb_img = image.load("Assets/modul_kerdesek/D/d_alap.png").convert_alpha()
d_gomb_action = (image.load("Assets/modul_kerdesek/D/d_kijelol.png").convert_alpha(), image.load("Assets/modul_kerdesek/D/d_benyom.png").convert_alpha())

progress_0_img = image.load("Assets/modul_kerdesek/allapot/progress_0.png").convert_alpha()
progress_1_img = image.load("Assets/modul_kerdesek/allapot/progress_1.png").convert_alpha()
progress_2_img = image.load("Assets/modul_kerdesek/allapot/progress_2.png").convert_alpha()
progress_3_img = image.load("Assets/modul_kerdesek/allapot/progress_3.png").convert_alpha()
progress_4_img = image.load("Assets/modul_kerdesek/allapot/progress_4.png").convert_alpha()

#Jelszó modul elmei

jelszo_modul_img = image.load("Assets/modul_jelszo/jelszo_224x224.png").convert_alpha()

#Liba mondja modul elmei

lib_mondja_modul_img = image.load("Assets/modul_libamondja/liba_mondja_224x224.png").convert_alpha()

allo_kek_img = image.load("Assets/modul_libamondja/allo/alap_kek_allo.png").convert_alpha()
allo_kek_img_action = (image.load("Assets/modul_libamondja/allo/kijelolt_kek_allo.png").convert_alpha(), image.load("Assets/modul_libamondja/allo/benyom_kek_allo.png").convert_alpha())
allo_piros_img = image.load("Assets/modul_libamondja/allo/alap_piros_allo.png").convert_alpha()
allo_piros_img_action = (image.load("Assets/modul_libamondja/allo/kijelolt_piros_allo.png").convert_alpha(), image.load("Assets/modul_libamondja/allo/benyom_piros_allo.png").convert_alpha())
allo_sarga_img = image.load("Assets/modul_libamondja/allo/alap_sarga_allo.png").convert_alpha()
allo_sarga_img_action = (image.load("Assets/modul_libamondja/allo/kijelolt_sarga_allo.png").convert_alpha(), image.load("Assets/modul_libamondja/allo/benyom_sarga_allo.png").convert_alpha())
allo_zold_img = image.load("Assets/modul_libamondja/allo/alap_zold_allo.png").convert_alpha()
allo_zold_img_action = (image.load("Assets/modul_libamondja/allo/kijelolt_zold_allo.png").convert_alpha(), image.load("Assets/modul_libamondja/allo/benyom_zold_allo.png").convert_alpha())

fekvo_kek_img = image.load("Assets/modul_libamondja/fekvo/alap_kek_fekvo.png").convert_alpha()
fekvo_kek_img_action = (image.load("Assets/modul_libamondja/fekvo/kijelolt_kek_fekvo.png").convert_alpha(), image.load("Assets/modul_libamondja/fekvo/benyom_kek_fekvo.png").convert_alpha())
fekvo_piros_img = image.load("Assets/modul_libamondja/fekvo/alap_piros_fekvo.png").convert_alpha()
fekvo_piros_img_action = (image.load("Assets/modul_libamondja/fekvo/kijelolt_piros_fekvo.png").convert_alpha(), image.load("Assets/modul_libamondja/fekvo/benyom_piros_fekvo.png").convert_alpha())
fekvo_sarga_img = image.load("Assets/modul_libamondja/fekvo/alap_sarga_fekvo.png").convert_alpha()
fekvo_sarga_img_action = (image.load("Assets/modul_libamondja/fekvo/kijelolt_sarga_fekvo.png").convert_alpha(), image.load("Assets/modul_libamondja/fekvo/benyom_sarga_fekvo.png").convert_alpha())
fekvo_zold_img = image.load("Assets/modul_libamondja/fekvo/alap_zold_fekvo.png").convert_alpha()
fekvo_zold_img_action = (image.load("Assets/modul_libamondja/fekvo/kijelolt_zold_fekvo.png").convert_alpha(), image.load("Assets/modul_libamondja/fekvo/benyom_zold_fekvo.png").convert_alpha())

#Időzítő modul elmei

idozito_modul_img = image.load("Assets/modul_idozito/idozito_224x224.png").convert_alpha()

#Bomba jellemzőinek elemei

szeriaszam_img = image.load("Assets/Egyeb/matricak_alap/szeria_alap.png").convert_alpha()
szeriaszam_kijelolve = image.load("Assets/Egyeb/matricak_alap/szeria_alap_kijelolve.png").convert_alpha()

nagy_szeria_matrica_img = image.load("Assets/Egyeb/matricak_nagyitva/szeria_nagyitva.png").convert_alpha()

matrica_fel_img = image.load("Assets/Egyeb/matricak_alap/matrica_fel.png").convert_alpha()
matrica_fel_kijelolve = image.load("Assets/Egyeb/matricak_alap/matrica_fel_kijelolve.png").convert_alpha()
matrica_le_img = image.load("Assets/Egyeb/matricak_alap/matrica_le.png").convert_alpha()
matrica_le_kijelolve = image.load("Assets/Egyeb/matricak_alap/matrica_le_kijelolve.png").convert_alpha()

nagy_feher_matrica_img = image.load("Assets/Egyeb/matricak_nagyitva/feher.png").convert_alpha()
nagy_fekete_matrica_img = image.load("Assets/Egyeb/matricak_nagyitva/fekete.png").convert_alpha()
nagy_narancs_matrica_img = image.load("Assets/Egyeb/matricak_nagyitva/narancs.png").convert_alpha()

elem_jobb_img = image.load("Assets/Egyeb/elemek/elem_jobb.png").convert_alpha()
elem_bal_img = image.load("Assets/Egyeb/elemek/elem_bal.png").convert_alpha()

#Dinamikus jelek elemei

jel_alap = image.load("Assets/Jelzok/alap_keret.png").convert_alpha()
jel_kijel = image.load("Assets/Jelzok/kijelol_keret.png").convert_alpha()
# jel_kat = image.load("Assets/Jelzok/kat_keret.png").convert_alpha()
jel_kesz = image.load("Assets/Jelzok/kesz_keret.png").convert_alpha()

jelek = (jel_alap, jel_kijel, jel_kesz)