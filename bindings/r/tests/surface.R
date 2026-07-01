library(nirs4all)

expected_exports <- c(
  "dag_ml",
  "dag_ml_data",
  "datasets",
  "formats",
  "io",
  "methods",
  "nirs4all_load_pipeline",
  "nirs4all_parse_execution_plan",
  "nirs4all_portable_class_names",
  "nirs4all_require",
  "nirs4all_run_portable_pipeline",
  "nirs4all_upstreams"
)

namespace <- asNamespace("nirs4all")
stopifnot(identical(packageDescription("nirs4all")$Package, "nirs4all"))
stopifnot(identical(sort(getNamespaceExports("nirs4all")), sort(expected_exports)))

for (name in expected_exports) {
  stopifnot(exists(name, envir = namespace, inherits = FALSE))
}

stopifnot(identical(nirs4all::formats, get("formats", envir = namespace)))
stopifnot(identical(nirs4all::methods, get("methods", envir = namespace)))
