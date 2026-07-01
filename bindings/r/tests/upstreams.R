library(nirs4all)

status <- nirs4all::nirs4all_upstreams()

stopifnot(identical(status$key, c("dag_ml", "dag_ml_data", "formats", "io", "datasets", "methods")))
stopifnot("candidates" %in% names(status))
stopifnot(grepl("n4m", status$candidates[status$key == "methods"], fixed = TRUE))

err <- tryCatch(nirs4all::nirs4all_require("missing"), error = identity)
stopifnot(inherits(err, "error"))

err <- tryCatch(nirs4all::dag_ml(), error = identity)
stopifnot(inherits(err, "error"))
