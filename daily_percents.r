library(plyr)

input_data_list <- list.files(path = "historical_data/csv_data", full.names = TRUE)
for (file in input_data_list) {
    input_data_frame <- ldply( .data = file,
                    .fun = read.csv,
                    header = TRUE,
                    col.names=c("Index","Date","Close","Volume","Open","High","Low") )
    input_data_frame[-1,]

    daily_close <- input_data_frame[3]
    daily_open <- input_data_frame[5]
    percent_change <- rep(NA, length(input_data_frame))
    percent_change <- daily_close/daily_open

}