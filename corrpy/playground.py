def clearNaN(df):
    df = df.dropna()
    return df

def infer_causal_direction(A, B):
    """
    Determines causal direction between A and B using LiNGAM.
    
    Args:
        A (array-like): Observations of variable A.
        B (array-like): Observations of variable B.
    
    Returns:
        tuple: Either (a, b) indicating A → B, or (b, a) indicating B → A.
    """
    # Stack data into (n_samples, 2) array
    data = np.column_stack((A, B))
    
    # Fit LiNGAM model
    model = DirectLiNGAM()
    model.fit(data)
    
    # Get adjacency matrix (shape: 2x2)
    adj_matrix = model.adjacency_matrix_
    
    # Check causal direction
    if adj_matrix[1, 0] != 0:  # A → B (row 1 is B, column 0 is A)
        return 1
    elif adj_matrix[0, 1] != 0:  # B → A (row 0 is A, column 1 is B)
        return 0
    else:
        return -1