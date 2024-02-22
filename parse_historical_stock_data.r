library(jsonlite)

input_data_list <- list.files(path = "/historical_data/json_data", full.names = TRUE)
for (file in input_data_list) {
    historical_data <- fromJSON(file)
    trades_table <- historical_data$data$tradesTable$rows

    framed_historical_data <- as.data.frame(trades_table)

    framed_historical_data <-
        as.data.frame(
            lapply(
                framed_historical_data,
                gsub,
                pattern = "$",
                fixed = TRUE,
                replacement = ""
            )
        )

    colnames(framed_historical_data) <-
    c("Date", "Close", "Volume", "Open", "High", "Low")
    framed_historical_data$Close <- as.numeric(framed_historical_data$Close)
    framed_historical_data$Open <- as.numeric(framed_historical_data$Open)
    framed_historical_data$High <- as.numeric(framed_historical_data$High)
    framed_historical_data$Low <- as.numeric(framed_historical_data$Low)

    ticker_name <- historical_data$data$symbol
    filename <- paste(ticker_name, ".csv", sep = "")
    filename <- file.path(paste(getwd(), "/historical_data/csv_data/", sep = ""), filename)

    write.csv(x = framed_historical_data, file = filename)

    plot(framed_historical_data$Close, xlab = "Date", ylab = "Closing Price")
    lines(framed_historical_data$Close)
}

