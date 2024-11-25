curl -XPOST -H "Content-type: application/json" -d '{
    "c_timesteps": 6,
    "global": {
        "CO2 limit": 150000000,
        "Cost limit": 35000000000
    },
    "site": {
        "Main": {
            "area": 20,
            "commodity": {
                "Solar": {
                    "Type": "SupIm"
                },
                "Wind": {
                    "Type": "SupIm"
                },
                "Elec": {
                    "Type": "Demand"
                },
                "CO2": {
                    "Type": "Env",
                    "price": 0,
                    "max": "inf",
                    "maxperhour": "inf"
                }
            },
            "process": {
                "Wind park": {
                    "inst-cap": 0,
                    "cap-lo": 0,
                    "cap-up": 20,
                    "max-grad": "inf",
                    "min-fraction": 3,
                    "inv-cost": 1000,
                    "fix-cost": 20,
                    "var-cost": 0,
                    "wacc": 0,
                    "depreciation": 25,
                    "commodity": {
                        "Wind": {
                            "Direction": "In",
                            "ratio": 1
                        },
                        "Elec": {
                            "Direction": "Out",
                            "ratio": 1
                        }
                    }
                },
                "Photovoltaics": {
                    "inst-cap": 0,
                    "cap-lo": 0,
                    "cap-up": 20,
                    "max-grad": "inf",
                    "min-fraction": 4,
                    "inv-cost": 300,
                    "fix-cost": 7,
                    "var-cost": 0,
                    "wacc": 0,
                    "depreciation": 25,
                    "area-per-cap": 1,
                    "commodity": {
                        "Solar": {
                            "Direction": "In",
                            "ratio": 1
                        },
                        "Elec": {
                            "Direction": "Out",
                            "ratio": 1
                        }
                    }
                }
            }
        }
    },
    "supim": {
        "Main": {
            "Wind": [
                1, 1, 1, 0, 0, 0
            ],
            "Solar": [
                0, 0, 0, 1, 1, 1
            ]
        }
    },
    "demand": {
        "Main": {
            "Elec": [
                10, 10, 10, 10, 10, 10
            ]
        }
    }
}' 'http://localhost:5000/simulate'