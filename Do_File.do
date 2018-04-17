cd "\\Client\C$\Users\Acer Valued Customer\Desktop\Kings Case Comp"
import delimited "\\Client\C$\Users\Acer Valued Customer\Desktop\Kings Case Comp\kings_case_comp\data\foul_trouble_data.csv"


gen minsquare = minremaining*minremaining
gen foulsquare = fouls*fouls
gen interaction = minremaining*fouls


regress index minremaining fouls
regress index minremaining fouls foulsquare
regress index minremaining fouls minsquare
regress index minremaining fouls interaction
regress index minremaining fouls foulsquare minsquare
regress index minremaining fouls foulsquare interaction
regress index minremaining fouls interaction minsquare
regress index minremaining fouls foulsquare minsquare interaction
