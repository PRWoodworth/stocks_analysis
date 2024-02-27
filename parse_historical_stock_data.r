library(jsonlite)

correct_datatypes <- function(framed_historical_data) {
    framed_historical_data$Close <- as.numeric(framed_historical_data$Close)
    framed_historical_data$Open <- as.numeric(framed_historical_data$Open)
    framed_historical_data$High <- as.numeric(framed_historical_data$High)
    framed_historical_data$Low <- as.numeric(framed_historical_data$Low)

    framed_historical_data$Date <- gsub("/", "", framed_historical_data$Date)
    framed_historical_data$Date <- as.Date(framed_historical_data$Date, "%m%d%Y")

    return(framed_historical_data)
}

add_daily_percents <- function(framed_historical_data){
    daily_close <- framed_historical_data$Close
    daily_open <- framed_historical_data$Open
    
    percent_change <- rep(NA, length(framed_historical_data))
    percent_change <- daily_close/daily_open

    framed_historical_data$Percent <- percent_change

    return(framed_historical_data)
}

input_data_list <- list.files(path = "historical_data/json_data", full.names = TRUE)
for (file in input_data_list) {
    historical_data <- fromJSON(file)
    data <- historical_data$data
    if(is.null(data)){
        next
    }
    
    trades_table <- data$tradesTable$rows
    if(is.null(trades_table)){
        next
    }
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

    colnames(framed_historical_data) <- c("Date", "Close", "Volume", "Open", "High", "Low")

    framed_historical_data <- correct_datatypes(framed_historical_data)
    framed_historical_data <- add_daily_percents(framed_historical_data)

    is_num <- sapply(framed_historical_data, is.numeric)
    framed_historical_data[is_num] <- lapply(framed_historical_data[is_num], round, 4)

    ticker_name <- historical_data$data$symbol
    filename <- paste(ticker_name, ".csv", sep = "")
    filename <- file.path(paste(getwd(), "/historical_data/csv_data/", sep = ""), filename)

    write.csv(x = framed_historical_data, file = filename)

    plot(y = framed_historical_data$Close, x = framed_historical_data$Date, xlab = "Date", ylab = "Close Price", type = "b")
}



