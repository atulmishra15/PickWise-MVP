import pandas as pd

def refine_recommendations(scored_df, prompt=None, top_n=12, price_min=None, price_max=None):
    """
    Refines buyability recommendations based on buyer input.
    
    Parameters:
    - scored_df: DataFrame with product info and buyability_score
    - prompt: String with refinement instructions (e.g. "more red, reduce browns")
    - top_n: Number of final recommendations to return
    - price_min: Optional price floor
    - price_max: Optional price ceiling
    
    Returns:
    - Refined DataFrame with top-N recommendations
    """

    df = scored_df.copy()

    # Price filtering
    if price_min is not None:
        df = df[df['price'] >= price_min]
    if price_max is not None:
        df = df[df['price'] <= price_max]

    # Handle color/attribute-based refinements
    if prompt:
        prompt = prompt.lower()

        # Example logic: adjust scores based on color mentions
        if "more red" in prompt:
            df['boost_red'] = df['color'].str.contains("red", case=False, na=False).astype(int)
            df['buyability_score'] += 0.1 * df['boost_red']
        if "fewer brown" in prompt:
            df['penalty_brown'] = df['color'].str.contains("brown", case=False, na=False).astype(int)
            df['buyability_score'] -= 0.1 * df['penalty_brown']
        if "more prints" in prompt:
            df['boost_print'] = df['print'].str.contains("print|pattern", case=False, na=False).astype(int)
            df['buyability_score'] += 0.1 * df['boost_print']
        if "reduce solid" in prompt:
            df['penalty_solid'] = df['print'].str.contains("solid", case=False, na=False).astype(int)
            df['buyability_score'] -= 0.1 * df['penalty_solid']

        # You can expand this logic with additional keywords

    # Final top-N selection
    df = df.sort_values(by='buyability_score', ascending=False).head(top_n)

    return df
# Build a logic that selects top N products with variety and completeness balance
