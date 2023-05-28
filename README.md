# Med_Normalization
Machine learning approach to Latvian medical text normalization

Šajā repozitorijā ir ievietoti kodu fragmenti, kas pielietoti mašīnmācīšanās metodes datu kopas un mT5 modeļa izstrādē.


contract_abbreviations:
  Satur kodu un datus, kas realizē saīsinājumu savēršanu medicīniskos tekstos.
  * main.py: veic galveno saīsinājumu savēršanu
  * split_data.py: veic atlasītās datu kopas sadalīšanu train/validate/test datu kopās
  * data: satur atlasītos medicīniskos teikumus un savēršamo terminu sarakstu

mT5_apmaciba:
  Satur kodu, kas realizē mT5 modeļa apmācību un testēšanu
  * fine_tune_mT5.py: Veic mT5 modeļa apmācību latviešu valodas medicīnisko tekstu normalizēšanai
  * run_test_dataset.py: Testē apmācīto mT5 modeli uz testēšanas datu kopu
  * speed_test.py: Salīdzina modeļa inferences laikus ar CPU un GPU
  * dataset: Satur modeļa apmācībā pielietoto datu kopu
  * > dataset/statistics: Satur informāciju par to cik termini un saīsinājumi atrasti pilnajā datu kopā (train/validate/test)

medical_atlase:
  Satur kodu, kas atbild par medicīnisko tekstu atlasi no pilnā Tīmeklis2020 korpusa.
  * keybert: Satur KeyBERT metodes realizāciju un no Tēzaura atlasītos medicīniskos terminus
  * dokumenti.py: Satur kodu, kas atlasa no Tīmeklis2020 korpusa tos dokumentus, kas satur medicīnisku terminu.
