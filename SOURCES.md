# Where the corpus comes from

`corpus.jsonl` has two parts, and every row says which one it belongs to in `source`.

## `grant_office_handbook` — GO-01 … GO-23

Written for this course. The Grant Office is the same **fictional** office as in HW2: the
eligibility rule in GO-02 and the amounts in GO-04 are the ones in HW2's `data/policy.json`.
No real university's rules are described here, and no model has seen this text in training,
which is exactly why it is here. Twenty are in English, one is in Kazakh (GO-14) and two are in
Russian (GO-15, GO-23).

## `wikipedia` — KZ-01 … KZ-51

The lead sections of 29 English Wikipedia articles about Kazakhstan, fetched through the
MediaWiki API on 2026-09-26 and split at paragraph boundaries into chunks of at most 170
words. The text is unedited apart from collapsed whitespace, so pronunciation guides and
other small artefacts of the plain-text export are still in it.

Wikipedia text is licensed under the Creative Commons Attribution-ShareAlike 4.0 licence
(CC BY-SA 4.0). These rows keep that licence, and each one carries its article's `url`.

| Article | Revision |
|---|---|
| [Kazakhstan](https://en.wikipedia.org/wiki/Kazakhstan) | 1376397836 |
| [Astana](https://en.wikipedia.org/wiki/Astana) | 1376397406 |
| [Almaty](https://en.wikipedia.org/wiki/Almaty) | 1375621927 |
| [Shymkent](https://en.wikipedia.org/wiki/Shymkent) | 1376270669 |
| [Baikonur Cosmodrome](https://en.wikipedia.org/wiki/Baikonur_Cosmodrome) | 1373460210 |
| [Kazakh language](https://en.wikipedia.org/wiki/Kazakh_language) | 1373817991 |
| [Kazakhstani tenge](https://en.wikipedia.org/wiki/Kazakhstani_tenge) | 1376259142 |
| [Lake Balkhash](https://en.wikipedia.org/wiki/Lake_Balkhash) | 1373177778 |
| [Aral Sea](https://en.wikipedia.org/wiki/Aral_Sea) | 1375412439 |
| [Charyn Canyon](https://en.wikipedia.org/wiki/Charyn_Canyon) | 1368966964 |
| [Nowruz](https://en.wikipedia.org/wiki/Nowruz) | 1376103377 |
| [Beshbarmak](https://en.wikipedia.org/wiki/Beshbarmak) | 1367707188 |
| [Dombra](https://en.wikipedia.org/wiki/Dombra) | 1356360187 |
| [Abai Qunanbaiuly](https://en.wikipedia.org/wiki/Abai_Qunanbaiuly) | 1375153942 |
| [Al-Farabi](https://en.wikipedia.org/wiki/Al-Farabi) | 1376722620 |
| [Kazakh Khanate](https://en.wikipedia.org/wiki/Kazakh_Khanate) | 1376832843 |
| [Tengiz Field](https://en.wikipedia.org/wiki/Tengiz_Field) | 1372805600 |
| [Kashagan Field](https://en.wikipedia.org/wiki/Kashagan_Field) | 1371472402 |
| [Medeu](https://en.wikipedia.org/wiki/Medeu) | 1375432228 |
| [Khan Tengri](https://en.wikipedia.org/wiki/Khan_Tengri) | 1369306943 |
| [Semipalatinsk Test Site](https://en.wikipedia.org/wiki/Semipalatinsk_Test_Site) | 1368578445 |
| [Kumis](https://en.wikipedia.org/wiki/Kumis) | 1376058376 |
| [Yurt](https://en.wikipedia.org/wiki/Yurt) | 1372847956 |
| [Kazakh alphabets](https://en.wikipedia.org/wiki/Kazakh_alphabets) | 1371140456 |
| [Narxoz University](https://en.wikipedia.org/wiki/Narxoz_University) | 1374369612 |
| [Caspian Sea](https://en.wikipedia.org/wiki/Caspian_Sea) | 1376689027 |
| [Altyn-Emel National Park](https://en.wikipedia.org/wiki/Altyn-Emel_National_Park) | 1362692178 |
| [Kazakh cuisine](https://en.wikipedia.org/wiki/Kazakh_cuisine) | 1371502616 |
| [Big Almaty Lake](https://en.wikipedia.org/wiki/Big_Almaty_Lake) | 1365908078 |
