SLAVE_SINGLE_REAL = 0
SLAVE_DIVERSE_REAL = 2
SLAVE_SINGLE_COMPLEX = 4
MASTER_SINGLE_REAL = 8
MASTER_DIVERSE_REAL = 10
MASTER_SINGLE_COMPLEX = 12

NCO_ACTIVE = 0            # NCO Active, Phase Amplitude dither disabled
NCO_BYPASS = 1            # NCO Bypass, Phase Amplitude dither disabled
NCO_ACTIVE_PD = 2         # NCO Active, Phase dither enabled
NCO_ACTIVE_AD = 4         # NCO Active, Amplitude dither enabled
NCO_ACTIVE_PAD = 6        # NCO Active, Phase Amplitude dither enabled

D300_OPT = [
    'MASTER SINGLE REAL',
    'MASTER DIVERSE REAL',
    'MASTER SINGLE COMPLEX',
    'SLAVE SINGLE REAL',
    'SLAVE DIVERSE REAL',
    'SLAVE SINGLE COMPLEX',
    ]

D300_DCT = {
    'MASTER SINGLE REAL': MASTER_SINGLE_REAL,
    'MASTER DIVERSE REAL': MASTER_DIVERSE_REAL,
    'MASTER SINGLE COMPLEX': MASTER_SINGLE_COMPLEX,
    'SLAVE SINGLE REAL': SLAVE_SINGLE_REAL,
    'SLAVE DIVERSE REAL': SLAVE_DIVERSE_REAL,
    'SLAVE SINGLE COMPLEX': SLAVE_SINGLE_COMPLEX,
    }

D301_OPT = [
    'ACTIVE',
    'BYPASS',
    'ACTIVE PHA DITHER',
    'ACTIVE AMP DITHER',
    'ACTIVE P/A DITHER',
    ]

D301_DCT = {
    'ACTIVE': NCO_ACTIVE,
    'BYPASS': NCO_BYPASS,
    'ACTIVE PHA DITHER': NCO_ACTIVE_PD,
    'ACTIVE AMP DITHER': NCO_ACTIVE_AD,
    'ACTIVE P/A DITHER': NCO_ACTIVE_PAD
    }

D302_DCT = {
    'MAX': 4_294_967_295,
    'MIN': 0,
    'DEFAULT': 0
}

D303_DCT = {
    'MAX': 4_294_967_295,
    'MIN': 0,
    'DEFAULT': 100_000
}

D304_DCT = {
    'MAX': 65_535,
    'MIN': 0,
    'DEFAULT': 0
}

D305_DCT = {
    'MAX': 6,
    'MIN': 0,
    'DEFAULT': 0
}

D306_DCT = {
    'MAX': 15,
    'MIN': 0,
    'DEFAULT': 0
}

D307_DCT = {
    'MAX': 20,
    'MIN': 0,
    'DEFAULT': 0
}

D308_DCT = {
    'MAX': 31,
    'MIN': 0,
    'DEFAULT': 0
}

D309_DCT = {
    'MAX': 7,
    'MIN': 0,
    'DEFAULT': 4
}

D30A_DCT = {
    'MAX': 31,
    'MIN': 0,
    'DEFAULT': 0
}

D30B_DCT = {
    'MAX': 127,
    'MIN': 0,
    'DEFAULT': 0
}

D30C_DCT = {
    'MAX': 255,
    'MIN': 0,
    'DEFAULT': 0
}

REGS_MAX = {
    '302': D302_DCT['MAX'],
    '303': D303_DCT['MAX'],
    '304': D304_DCT['MAX'],
    '305': D305_DCT['MAX'],
    '306': D306_DCT['MAX'],
    '307': D307_DCT['MAX'],
    '308': D308_DCT['MAX'],
    '309': D309_DCT['MAX'],
    '30A': D30A_DCT['MAX'],
    '30B': D30B_DCT['MAX'],
    '30C': D30C_DCT['MAX'],
}

REGS_MIN = {
    '302': D302_DCT['MIN'],
    '303': D303_DCT['MIN'],
    '304': D304_DCT['MIN'],
    '305': D305_DCT['MIN'],
    '306': D306_DCT['MIN'],
    '307': D307_DCT['MIN'],
    '308': D308_DCT['MIN'],
    '309': D309_DCT['MIN'],
    '30A': D30A_DCT['MIN'],
    '30B': D30B_DCT['MIN'],
    '30C': D30C_DCT['MIN'],
}

REGS_DEFAULT = {
    '302': D302_DCT['DEFAULT'],
    '303': D303_DCT['DEFAULT'],
    '304': D304_DCT['DEFAULT'],
    '305': D305_DCT['DEFAULT'],
    '306': D306_DCT['DEFAULT'],
    '307': D307_DCT['DEFAULT'],
    '308': D308_DCT['DEFAULT'],
    '309': D309_DCT['DEFAULT'],
    '30A': D30A_DCT['DEFAULT'],
    '30B': D30B_DCT['DEFAULT'],
    '30C': D30C_DCT['DEFAULT'],
}
