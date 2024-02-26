library( plyr )

input_data_list <- list.files(path = "historical_data/csv_data", full.names = TRUE)
for (file in input_data_list) {
    input_data_frame <- ldply( .data = file,
                    .fun = read.csv,
                    header = FALSE,
                    col.names=c("Index","Date","Close","Volume","Open","High","Low") )
    for (i in 1:nrow(input_data_frame)){
        daily_open <- c()
        daily_close <- c()
        daily_percent <- c()

        
    }
}