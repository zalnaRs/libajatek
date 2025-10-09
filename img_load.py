from pygame import image

background_img = image.load("Backs/background.png").convert_alpha()
start_background_img = image.load("Backs/start.png").convert_alpha()

resume_img = image.load("Buttons/resume_button.png").convert_alpha()
resume_le = image.load("Buttons/resume_button_le.png").convert_alpha()
quit_img = image.load("Buttons/quit_button.png").convert_alpha()
quit_le = image.load("Buttons/quit_button_le.png").convert_alpha()
start_img = image.load("Buttons/start_button.png").convert_alpha()
start_le = image.load("Buttons/start_button_le.png").convert_alpha()
back_img = image.load("Buttons/back_button.png").convert_alpha()
back_le = image.load("Buttons/back_button_le.png").convert_alpha()
sz1_img = image.load("Buttons/1_button.png").convert_alpha()
sz1_le = image.load("Buttons/1_button_le.png").convert_alpha()
sz2_img = image.load("Buttons/2_button.png").convert_alpha()
sz2_le = image.load("Buttons/2_button_le.png").convert_alpha()
sz3_img = image.load("Buttons/3_button.png").convert_alpha()
sz3_le = image.load("Buttons/3_button_le.png").convert_alpha()
sz4_img = image.load("Buttons/4_button.png").convert_alpha()
sz4_le = image.load("Buttons/4_button_le.png").convert_alpha()
left_img = image.load("Buttons/balra.png").convert_alpha()
left_kijelolve = image.load("Buttons/balra_kijelolve.png").convert_alpha()
right_img = image.load("Buttons/jobbra.png").convert_alpha()
right_kijelolve = image.load("Buttons/jobbra_kijelolve.png").convert_alpha()

bomba_img = image.load("Backs/bomba_alap.png").convert_alpha()

sima_drot_modul_img = image.load("nat_drotok/drot_nat_224x224.png").convert_alpha()

fekete_drot_img = image.load("nat_drotok/fekete/fekete_alap.png").convert_alpha()
fekete_drot_action = (image.load("nat_drotok/fekete/fekete_kijelolve.png").convert_alpha(), image.load("nat_drotok/fekete/fekete_vagas.png").convert_alpha(), image.load("nat_drotok/fekete/fekete_kesz.png").convert_alpha())
kek_drot_img = image.load("nat_drotok/kek/kek_alap.png").convert_alpha()
kek_drot_action = (image.load("nat_drotok/kek/kek_kijelolve.png").convert_alpha(), image.load("nat_drotok/kek/kek_vagas.png").convert_alpha(), image.load("nat_drotok/kek/kek_kesz.png").convert_alpha())
piros_drot_img = image.load("nat_drotok/piros/piros_alap.png").convert_alpha()
piros_drot_action = (image.load("nat_drotok/piros/piros_kijelolve.png").convert_alpha(), image.load("nat_drotok/piros/piros_vagas.png").convert_alpha(), image.load("nat_drotok/piros/piros_kesz.png").convert_alpha())
sarga_drot_img = image.load("nat_drotok/sarga/sarga_alap.png").convert_alpha()
sarga_drot_action = (image.load("nat_drotok/sarga/sarga_kijelolve.png").convert_alpha(), image.load("nat_drotok/sarga/sarga_vagas.png").convert_alpha(), image.load("nat_drotok/sarga/sarga_kesz.png").convert_alpha())

komplex_kabel_modul_img = image.load("kom_kabel/kabel_kom_224x224.png").convert_alpha()

kabel_1_img = image.load("kom_kabel/1_kabel/1_alap.png").convert_alpha()
kabel_1_action = (image.load("kom_kabel/1_kabel/1_kijelolve.png").convert_alpha(), image.load("kom_kabel/1_kabel/1_vagas.png").convert_alpha(), image.load("kom_kabel/1_kabel/1_kesz.png").convert_alpha())
kabel_2_img = image.load("kom_kabel/2_kabel/2_alap.png").convert_alpha()
kabel_2_action = (image.load("kom_kabel/2_kabel/2_kijelolve.png").convert_alpha(), image.load("kom_kabel/2_kabel/2_vagas.png").convert_alpha(), image.load("kom_kabel/2_kabel/2_kesz.png").convert_alpha())
kabel_3_img = image.load("kom_kabel/3_kabel/3_alap.png").convert_alpha()
kabel_3_action = (image.load("kom_kabel/3_kabel/3_kijelolve.png").convert_alpha(), image.load("kom_kabel/3_kabel/3_vagas.png").convert_alpha(), image.load("kom_kabel/3_kabel/3_kesz.png").convert_alpha())
kabel_4_img = image.load("kom_kabel/4_kabel/4_alap.png").convert_alpha()
kabel_4_action = (image.load("kom_kabel/4_kabel/4_kijelolve.png").convert_alpha(), image.load("kom_kabel/4_kabel/4_vagas.png").convert_alpha(), image.load("kom_kabel/4_kabel/4_kesz.png").convert_alpha())

gomb_modul_img = image.load("gomb_modul/gomb_alap_224x224.png").convert_alpha()

kek_gomb_img = image.load("gomb_modul/kek/kek_sima.png").convert_alpha()
kek_gomb_action = (image.load("gomb_modul/kek/kek_kijelol.png").convert_alpha(), image.load("gomb_modul/kek/kek_benyomva.png").convert_alpha(), image.load("gomb_modul/kek/kek_kesz.png").convert_alpha())
piros_gomb_img = image.load("gomb_modul/piros/piros_sima.png").convert_alpha()
piros_gomb_action = (image.load("gomb_modul/piros/piros_kijelol.png").convert_alpha(), image.load("gomb_modul/piros/piros_benyomva.png").convert_alpha(), image.load("gomb_modul/piros/piros_kesz.png").convert_alpha())
zold_gomb_img = image.load("gomb_modul/zold/zold_sima.png").convert_alpha()
zold_gomb_action = (image.load("gomb_modul/zold/zold_kijelol.png").convert_alpha(), image.load("gomb_modul/zold/zold_benyomva.png").convert_alpha(), image.load("gomb_modul/zold/zold_kesz.png").convert_alpha())

lud_szimbolum = image.load("gomb_modul/szimbolumok/minta_lud.png").convert_alpha()
talp_szimbolum = image.load("gomb_modul/szimbolumok/minta_talp.png").convert_alpha()
tojas_szimbolum = image.load("gomb_modul/szimbolumok/minta_tojas.png").convert_alpha()

kerdes_modul_img = image.load("kerdesek/kerdesek_panel.png").convert_alpha()

a_gomb_img = image.load("kerdesek/A/a_alap.png").convert_alpha()
a_gomb_action = (image.load("kerdesek/A/a_kijelol.png").convert_alpha(), image.load("kerdesek/A/a_benyom.png").convert_alpha())
b_gomb_img = image.load("kerdesek/B/b_alap.png").convert_alpha()
b_gomb_action = (image.load("kerdesek/B/b_kijelol.png").convert_alpha(), image.load("kerdesek/B/b_benyom.png").convert_alpha())
c_gomb_img = image.load("kerdesek/C/c_alap.png").convert_alpha()
c_gomb_action = (image.load("kerdesek/C/c_kijelol.png").convert_alpha(), image.load("kerdesek/C/c_benyom.png").convert_alpha())
d_gomb_img = image.load("kerdesek/D/d_alap.png").convert_alpha()
d_gomb_action = (image.load("kerdesek/D/d_kijelol.png").convert_alpha(), image.load("kerdesek/D/d_benyom.png").convert_alpha())

progress_0_img = image.load("kerdesek/allapot/progress_0.png").convert_alpha()
progress_1_img = image.load("kerdesek/allapot/progress_1.png").convert_alpha()
progress_2_img = image.load("kerdesek/allapot/progress_2.png").convert_alpha()
progress_3_img = image.load("kerdesek/allapot/progress_3.png").convert_alpha()
progress_4_img = image.load("kerdesek/allapot/progress_4.png").convert_alpha()

jelszo_modul_img = image.load("jelszo/jelszo_modul.png").convert_alpha()

lud_mondja_modul_img = image.load("simon/szines.png").convert_alpha()

allo_kek_img = image.load("simon/allo/alap_kek_allo.png").convert_alpha()
allo_kek_img_action = (image.load("simon/allo/kijelolt_kek_allo.png").convert_alpha(), image.load("simon/allo/benyom_kek_allo.png").convert_alpha())
allo_piros_img = image.load("simon/allo/alap_piros_allo.png").convert_alpha()
allo_piros_img_action = (image.load("simon/allo/kijelolt_piros_allo.png").convert_alpha(), image.load("simon/allo/benyom_piros_allo.png").convert_alpha())
allo_sarga_img = image.load("simon/allo/alap_sarga_allo.png").convert_alpha()
allo_sarga_img_action = (image.load("simon/allo/kijelolt_sarga_allo.png").convert_alpha(), image.load("simon/allo/benyom_sarga_allo.png").convert_alpha())
allo_zold_img = image.load("simon/allo/alap_zold_allo.png").convert_alpha()
allo_zold_img_action = (image.load("simon/allo/kijelolt_zold_allo.png").convert_alpha(), image.load("simon/allo/benyom_zold_allo.png").convert_alpha())

fekvo_kek_img = image.load("simon/fekvo/alap_kek_fekvo.png").convert_alpha()
fekvo_kek_img_action = (image.load("simon/fekvo/kijelolt_kek_fekvo.png").convert_alpha(), image.load("simon/fekvo/benyom_kek_fekvo.png").convert_alpha())
fekvo_piros_img = image.load("simon/fekvo/alap_piros_fekvo.png").convert_alpha()
fekvo_piros_img_action = (image.load("simon/fekvo/kijelolt_piros_fekvo.png").convert_alpha(), image.load("simon/fekvo/benyom_piros_fekvo.png").convert_alpha())
fekvo_sarga_img = image.load("simon/fekvo/alap_sarga_fekvo.png").convert_alpha()
fekvo_sarga_img_action = (image.load("simon/fekvo/kijelolt_sarga_fekvo.png").convert_alpha(), image.load("simon/fekvo/benyom_sarga_fekvo.png").convert_alpha())
fekvo_zold_img = image.load("simon/fekvo/alap_zold_fekvo.png").convert_alpha()
fekvo_zold_img_action = (image.load("simon/fekvo/kijelolt_zold_fekvo.png").convert_alpha(), image.load("simon/fekvo/benyom_zold_fekvo.png").convert_alpha())

visszaszamlalo_img = image.load("idozito/idozito.png").convert_alpha()

szeriaszam_img = image.load("egyeb/matricak_alap/szeria_alap.png").convert_alpha()
szeriaszam_kijelolve = image.load("egyeb/matricak_alap/szeria_alap_kijelolve.png").convert_alpha()

nagy_szeria_matrica_img = image.load("egyeb/matricak_nagyitva/szeria_nagyitva.png").convert_alpha()

matrica_fel_img = image.load("egyeb/matricak_alap/matrica_fel.png").convert_alpha()
matrica_fel_kijelolve = image.load("egyeb/matricak_alap/matrica_fel_kijelolve.png").convert_alpha()
matrica_le_img = image.load("egyeb/matricak_alap/matrica_le.png").convert_alpha()
matrica_le_kijelolve = image.load("egyeb/matricak_alap/matrica_le_kijelolve.png").convert_alpha()

nagy_feher_matrica_img = image.load("egyeb/matricak_nagyitva/feher.png").convert_alpha()
nagy_fekete_matrica_img = image.load("egyeb/matricak_nagyitva/fekete.png").convert_alpha()
nagy_narancs_matrica_img = image.load("egyeb/matricak_nagyitva/narancs.png").convert_alpha()

elem_jobb_img = image.load("egyeb/elemek/elem_jobb.png").convert_alpha()
elem_bal_img = image.load("egyeb/elemek/elem_bal.png").convert_alpha()

jel_alap = image.load("Jelzok/alap_keret.png").convert_alpha()
jel_kijel = image.load("Jelzok/kijelol_keret.png").convert_alpha()
# jel_kat = image.load("Jelzok/kat_keret.png").convert_alpha()
jel_kesz = image.load("Jelzok/kesz_keret.png").convert_alpha()

jelek = (jel_alap, jel_kijel, jel_kesz)