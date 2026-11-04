.PHONY: data plot-data fit \
        plot-boundaries boundaries plot-confusion-moons plot-depth-moons \
        cv-moons \
        install submit clean clean-results clean-datasets

DATASETS = moons circles xor checkerboard linear


# ---- Task C Data ------------------------------------------------------------

data:
	uv run python scripts/create_datasets.py all

plot-data:
	uv run python scripts/plotting/plot_datasets.py $(DATASETS) \
		--save results/figures/datasets.png


# ---- Task D Fitting ---------------------------------------------------------

fit:
	uv run python scripts/fit_tree.py $(DATASETS) --criterion gini


# ---- Task E Evaluation ------------------------------------------------------

plot-boundaries:
	uv run python scripts/plotting/plot_boundary_grid.py $(DATASETS) \
		--depths 1 2 4 8 None --save results/figures/boundaries.png

boundaries: data fit plot-boundaries

plot-confusion-moons:
	uv run python scripts/plotting/plot_confusion_matrix.py moons \
		--save results/figures/confusion_moons.png

plot-depth-moons:
	uv run python scripts/plotting/plot_depth_accuracy.py moons \
		--save results/figures/depth_accuracy_moons.png


# ---- Task F Development -----------------------------------------------------

cv-moons:
	uv run python scripts/cv_gridsearch.py moons \
		--criterion gini entropy --max-depth 1 2 4 6 8 None --folds 5


# ---- Utilities --------------------------------------------------------------

install:
	uv sync
	git init -b main
	uv run pre-commit install

# Writes submission.json with every answer in worksheet.py.
submit:
	uv run python submit.py

clean:
	rm -rf .venv .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

clean-results:
	rm -rf results

clean-datasets:
	rm -rf data
