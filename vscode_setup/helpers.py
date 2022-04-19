"""Helper functions for the GCP scripts."""

def progress_bar(
    iteration: int, 
    total: int,
    prefix: str = '',
    suffix: str = '',
    decimals: int = 1,
    length: int = 100,
    fill: str = '█',
) -> None:
    """
    Call in a loop to create terminal progress bar.
    
    Parameters:
        iteration: int
            current iteration
        total: int
            total iterations
        prefix: optional str, default ''
            prefix string
        suffix: optional str, default ''
            suffix string
        decimals: optional int, default 1
            positive number of decimals in percent complete
        length: optional int, default 100
            character length of bar
        fill: optional str, default '█'
            bar fill character

    Returns:
        None
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print('Completed.')
        