# TauPOG Corrections

These are the JSON files for the TauPOG. The are created with the scripts in [`scripts/`](../../scripts).


## Summary of available DeepTau SFs

This is a rough summary of the available SFs for `DeepTau2017v2p1` from the [official TauPOG SF tool](https://github.com/cms-tau-pog/TauIDSFs/tree/master/data)

| Tau component  | `genmatch`  | `DeepTau2017v2p1` `VSjet`  | `DeepTau2017v2p1` `VSe`  | `DeepTau2017v2p1` `VSmu`  | energy scale   |
|:--------------:|:-----------:|:--------------------------:|:------------------------:|:-------------------------:|:--------------:|
| real tau       | `5`         | vs. pT, or vs. DM          | –                        | –                         | vs. DM         |
| e -> tau fake  | `1`, `3`    | –                          | vs. eta                  | –                         | vs. DM and eta |
| mu -> tau fake | `2`, `4`    | –                          | –                        | vs. eta                   | – (±1% unc.)   |


## Structure of e -> tau fake rate SFs
One JSON file per ID and year.
```
ID (e.g. antiEle, DeepTau2017v2p1VSe)
└─ year
   └─ category:genmatch (0-5)
      ├─ key:genmatch==1,3 (e -> tau fake)
      │  └─ category:WP
      │     └─ binned:abseta
      │        └─ category:syst (nom, up, down)
      │           └─ float:SF
      └─ key:default (genmatch!=1,3)
         └─ float:SF
```


## Structure of mu -> tau fake rate SFs
One JSON file per ID and year.
```
ID (e.g. antiMu, DeepTau2017v2p1VSmu)
└─ year
   └─ category:genmatch (0-5)
      ├─ key:genmatch==2,4 (mu -> tau fake)
      │  └─ category:WP
      │     └─ category:syst (nom, up, down)
      │        └─ binned:abseta
      │           └─ float:SF
      └─ key:default (genmatch!=2,4)
         └─ float:SF
```


## Structure of real tau efficiency rate SFs
One JSON file per ID and year.
Users can choose either pT- __or__ DM-dependent SFs.
```
ID (e.g. MVAoldDM2017v2, DeepTau2017v2p1VSjet)
└─ year
   └─ category:genmatch (0-5)
      ├─ key:genmatch==5 (real tau)
      │  ├─ pT-dependent
      │  │  └─ category:syst (nom, up, down)
      │  │     └─ TFormula
      │  └─ DM-dependent
      │     └─ category:DM
      │        └─ category:syst (nom, up, down)
      │           └─ float:SF
      └─ key:default (genmatch!=5)
         └─ float:SF
```

<p align="center">
  <img src="../../docs/Tau_SF_vs_pt.gif" alt="Tau DeepTau2017v2VSjet efficiency SF" width="380"/>
</p>


## Structure of tau energy scales
One JSON file per ID and year.
```
year
└─ category:genmatch
   ├─ key:genmatch==5 (real tau)
   │  └─ category:DM
   │     └─ category:syst (nom, up, down)
   │        └─ TFormula
   ├─ key:genmatch==1,3 (e -> tau fake)
   │  └─ category:DM
   │     └─ binned:eta
   │        └─ category:syst (nom, up, down)
   │           └─ float:SF
   └─ key:genmatch==2,4 (muon)
      └─ category:syst (nom, up, down)
         └─ float:SF
```

<p align="center">
  <img src="../../docs/TESunc.png" alt="Tau energy scale uncertainty treatment" width="380"/>
</p>


## Structure of tau triggers
TBA.
