# Rearrange / concat https://beta.openai.com/playground/p/spY0oKIjkSga7aNVOVQR0L2N?model=davinci-instruct-beta

REFORMAT_TABLE_DATASET_TRAIN = """

Format the following tables based on user commands

TABLE
| Fruit | Color | Flavor |
| Neoskizzles | Purple | Sweet |
| Loheckles | Grayish blue | Tart |

COMMAND
Only display the fruit and color columns

OUTPUT
| Fruit | Color |
| Neoskizzles | Purple |
| Loheckles | Grayish blue |
<<END>>

TABLE
| Language | Difficulty | 
| C | Easy |
| Java | Medium |
| C++ | Hard |
| Perl | Easy |
| Python | Easy |

COMMAND
Display the Difficulty column first followed by language. Add a new column which concatenates difficulty and language.

OUTPUT
| Difficulty | Language |
| Easy |C | EasyC |
| Medium | Java |MediumJava |
| Hard | C++ | HardC++ |
| Easy | Perl | EasyPerl |
| Easy | Python | EasyPython |
<<END>>

TABLE
| date | subject | from |
| 2021-02-10 | Hey that's cool | bfortuner@gmail.com |
| 2020-13-01 | Re: Refund order | mission@bodyrok.com |
| 2021-02-12 | Tennis match | chgas1@hotmail.com |
| 2021-08-03 |This is a longer subject than usual | andrew.kouri@lvl5.ai |

COMMAND
Only display the date column

OUTPUT
| date |
| 2021-08-03 |
| 2021-02-12 |
| 2021-02-10 |
| 2020-13-01 |
<<END>>

TABLE
| row_id | cost | merchant |
| 1 | -10 | McDonalds |
| 2 | 3.23 | HenryAndCompany |
| 3 | 1239.02 | Marshmellow |
| 4 | 0.23 | Variety |

COMMAND
Only display the cost column

OUTPUT
| cost |
| -10 |
| 3.23 |
| 1239.02 |
| 0.23 |
<<END>>

TABLE
| row_id | cost | merchant |
| 1 | -10 | McDonalds |
| 2 | 3.23 | HenryAndCompany |
| 3 | 1239.02 | Marshmellow |
| 4 | 0.23 | Variety |

COMMAND
Add a new column which concatenates cost and merchant called "joined"

OUTPUT
| row_id | cost | merchant | joined |
| 1 | -10 | McDonalds | -10McDonalds |
| 2 | 3.23 | HenryAndCompany | 3.23HenryAndCompany |
| 3 | 1239.02 | Marshmellow | 1239.02Marshmellow |
| 4 | 0.23 | Variety | 0.23Variety |

"""