"""
Aggregate insurance loss model using a compound
Poisson-Lognormal frequency-severity framework.

Author: Ruben
"""

#imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

np.random.seed(42)

pd.set_option("display.max_columns", None) 

# Project directories

BASE_DIR = Path(__file__).resolve().parent

PLOT_DIR = BASE_DIR / "results" / "plots"
TABLE_DIR = BASE_DIR / "results" / "tables"

# Create folders if they do not exist

PLOT_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)

def apply_excess_of_loss(claims, attachment, limit):
    """
    Apply a per-claim excess-of-loss reinsurance contract.

    Each claim is reduced according to an excess layer with a
    specified attachment point and limit.

    Parameters
    ----------
    claims : numpy.ndarray
        Array of gross individual claim amounts.
    attachment : float
        Excess attachment point. Losses below this value are not covered.
    limit : float
        Maximum amount recoverable from the reinsurer per claim.

    Returns
    -------
    numpy.ndarray
        Array of ceded claim amounts after applying the excess-of-loss layer.
    """

    ceded_claims = np.minimum(
        np.maximum(claims - attachment, 0),
        limit
    )

    return ceded_claims

def simulate_losses(years, claim_frequency, log_mean, log_sigma):
    """
    Simulate annual aggregate insurance losses using a
    compound Poisson-Lognormal model.

    Parameters
    ----------
    years : int
        Number of simulated years.
    claim_frequency : float
        Expected number of claims per year (Poisson lambda).
    log_mean : float
        Mean parameter of lognormal severity distribution.
    log_sigma : float
        Standard deviation parameter of lognormal severity distribution.

    Returns
    -------
    numpy.ndarray
        Simulated annual aggregate losses.
    """

    total_loss = []

    for _ in range(years):

        N = np.random.poisson(lam=claim_frequency)

        claims = np.random.lognormal(
            mean=log_mean,
            sigma=log_sigma,
            size=N
        )
        
        ceded_claims = apply_excess_of_loss(
            claims,
            attachment=10000,
            limit=50000
        )

        retained_claims = claims - ceded_claims
    
        loss = np.sum(retained_claims)

        total_loss.append(loss)

    return np.array(total_loss)


def summary_statistics(total_loss):
    """
    Calculate summary statistics for simulated losses.

    Returns
    -------
    tuple
        Mean, standard deviation, maximum and minimum loss.
    """

    mean = np.mean(total_loss)
    standard_deviation = np.std(total_loss)
    maximum = np.max(total_loss)
    minimum = np.min(total_loss)

    return mean, standard_deviation, maximum, minimum


def probability_exceedance(total_loss, threshold):
    """
    Calculate probability that losses exceed a threshold.
    """

    return np.mean(total_loss > threshold)


def risk_measure(total_loss):
    """
    Calculate Value-at-Risk at 95% and 99% confidence levels.
    """

    var95 = np.percentile(total_loss, 95)
    var99 = np.percentile(total_loss, 99)

    return var95, var99


def expected_shortfall(total_loss, confidence):
    """
    Calculate Expected Shortfall at a given confidence level.
    """

    var = np.percentile(total_loss, confidence)

    losses_above_var = total_loss[total_loss > var]

    return np.mean(losses_above_var)


def plot_loss_distribution(total_loss):
    """
    Plot annual aggregate loss distribution.
    """

    plt.figure(figsize=(8, 5))

    plt.hist(
        total_loss,
        bins=50,
        edgecolor="black"
    )

    plt.xlabel("Annual Total Loss (£)")
    plt.ylabel("Frequency")
    plt.title("Annual Aggregate Loss Distribution")
    plt.grid(True)

    plt.savefig(
        PLOT_DIR / "loss_distribution.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show() 
    
def plot_claim_severity(log_mean, log_sigma):
    """
    Plot the simulated lognormal claim severity distribution.

    Parameters
    ----------
    log_mean : float
        Mean parameter of the lognormal severity distribution.
    log_sigma : float
        Standard deviation parameter of the lognormal severity distribution.
    """

    claims = np.random.lognormal(
        mean=log_mean,
        sigma=log_sigma,
        size=10000
    )

    plt.hist(
        claims,
        bins=50,
        density = True,
        edgecolor="black"
    )
    
    plt.xlim(0, 20000)

    plt.xlabel("Claim Amount (£)")
    plt.ylabel("Density")
    plt.title("Lognormal Claim Severity Distribution")

    plt.savefig(
        PLOT_DIR / "claim_severity.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def main():

    # Model parameters

    years = 100000

    log_mean = 7
    log_sigma = 1

    confidence = 99

    frequencies = [5, 10, 15, 20]


    results = []

    all_losses = {}


    # Sensitivity analysis

    for claim_frequency in frequencies:

        total_loss = simulate_losses(
            years,
            claim_frequency,
            log_mean,
            log_sigma
        )

        all_losses[claim_frequency] = total_loss


        mean, sd, maximum, minimum = summary_statistics(total_loss)


        var95, var99 = risk_measure(total_loss)

        es = expected_shortfall(
            total_loss,
            confidence
        )


        results.append(
            [
                claim_frequency,
                mean,
                var95,
                var99,
                es
            ]
        )


    # Create results dataframe

    df = pd.DataFrame(
        results,
        columns=[
            "Claim Frequency (Lambda)",
            "Mean Annual Loss",
            "VaR 95%",
            "VaR 99%",
            f"ES {confidence}%"
        ]
    )


    print(
        df.to_string(
            formatters={
                "Mean Annual Loss": "£{:,.2f}".format,
                "VaR 95%": "£{:,.2f}".format,
                "VaR 99%": "£{:,.2f}".format,
                f"ES {confidence}%": "£{:,.2f}".format
            }
        )
    )


    # Save table

    df.to_csv(
        TABLE_DIR / "aggregate_claim_results.csv",
        index=False
    )


    # Plot distributions

    plt.figure(figsize=(8,5))

    for frequency in frequencies:

        plt.hist(
            all_losses[frequency],
            bins=50,
            alpha=0.5,
            label=f"lambda = {frequency}"
        )

    plt.xlabel("Annual Total Loss (£)")
    plt.ylabel("Frequency")
    plt.title("Aggregate Loss Distribution for Different Claim Frequencies")
    plt.legend()
    plt.grid(True)

    plt.savefig(
        PLOT_DIR / "frequency_sensitivity_distribution.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()


    # Mean loss sensitivity plot

    plt.figure(figsize=(8,5))

    plt.plot(
        df["Claim Frequency (Lambda)"],
        df["Mean Annual Loss"],
        marker="o"
    )

    plt.xlabel("Claim Frequency (Lambda)")
    plt.ylabel("Mean Annual Loss (£)")
    plt.title("Claim Frequency vs Mean Annual Loss")
    plt.grid(True)

    plt.savefig(
        PLOT_DIR / "mean_loss_sensitivity.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


    # VaR sensitivity plot

    plt.figure(figsize=(8,5))

    plt.plot(
        df["Claim Frequency (Lambda)"],
        df["VaR 99%"],
        marker="o"
    )

    plt.xlabel("Claim Frequency (Lambda)")
    plt.ylabel("VaR 99% (£)")
    plt.title("Claim Frequency vs VaR 99%")
    plt.grid(True)

    plt.savefig(
        PLOT_DIR / "var99_sensitivity.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


    # Single distribution plot

    plot_loss_distribution(
        all_losses[10]
    ) 
    
    plot_claim_severity(
        log_mean,
        log_sigma
    )


if __name__ == "__main__":
    main()




