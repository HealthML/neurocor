

from argparse import ArgumentParser
import numpy as np
import pandas as pd

def cleanup_summary_statistics(df):
    """Reformat the summary statistics download from the GWAS catalog
    Args:
        df: The dataframe of summary statistics downloaded from the GWAS catalog
    """
    # rename the columns to those used by https://github.com/bulik/ldsc/blob/master/munge_sumstats.py
    # this won't do anything if the columns already have the correct names
    rename_cols = {'hm_rsid':'SNP',
                   'chromosome':'CHR',
                   'base_pair_location':'BP',
                   'p_value':'P',
                   'standard_error': 'SD',
                   'effect_allele':'A1', 
                   'other_allele':'A2', 
                   'odds_ratio':'OR', 
                   'beta':'BETA', 
                   'effect_allele_frequency':'FRQ',
                   'n':'N',
                   'z':'Z'}
    
    df = df.rename(columns=rename_cols)
    
    # below some efforts are made to recover columns from summary statistics if they don't follow the recommended naming convention.

    if 'CHR' not in df.columns:
        chr_cols = list(c for c in df.columns if str(c).lower().startswith('chrom'))
        chr_cols += list(c for c in df.columns if str(c).lower().startswith('chr'))
        if len(chr_cols):
            print('Assuming "{}" is the CHR column'.format(chr_cols[0]))
            df.rename(columns={chr_cols[0]:'CHR'}, inplace=True)
    
    if 'BP' not in df.columns:
        pos_cols = list(c for c in df.columns if str(c).lower().startswith('pos'))
        pos_cols += list(c for c in df.columns if str(c).lower() == 'bp')
        if len(pos_cols):
            print('Assuming "{}" is the BP column'.format(pos_cols[0]))
            df.rename(columns={pos_cols[0]:'BP'}, inplace=True)
        else:
            print('Warning: could not find the BP (position) column.')
    
    if 'SNP' not in df.columns:
        snp_cols = list(c for c in df.columns if 'rsid' in str(c).lower())
        snp_cols += list(c for c in df.columns if 'variant_id' == str(c).lower())
        snp_cols += list(c for c in df.columns if str(c).lower().startswith('snp'))
        if len(snp_cols):
            print('Assuming "{}" is the SNP column'.format(snp_cols[0]))
            df.rename(columns={snp_cols[0]:'SNP'}, inplace=True)
        else:
            print('Unable to determine the SNP column. Using dummy values.')
            df['SNP'] = np.array(['snp_{}'.format(i) for i in range(len(df))])
                
    if 'A1' not in df.columns:
        a1_cols = []
        if 'ALLELE1' in df.columns:
            a1_cols = ['ALLELE1']
        a1_cols += list(c for c in df.columns if str(c).lower().startswith('a1') and ('freq' not in  str(c).lower()) and ('frq' not in str(c).lower()))
        a1_cols += list(c for c in df.columns if str(c).lower().startswith('allele') and str(c).endswith('1'))
        a1_cols += list(c for c in df.columns if str(c).lower().startswith('effect') and str(c).lower().endswith('allele'))
        a1_cols += list(c for c in df.columns if str(c).lower().startswith('alter') and str(c).lower().endswith('allele'))
        a1_cols += list(c for c in df.columns if str(c).lower().startswith('minor') and str(c).lower().endswith('allele'))
        if len(a1_cols):
            if len(a1_cols) > 1:
                print('Warning: found multiple possible columns containing A1 : {}'.format(a1_cols))
            print('Assuming "{}" is the A1 column'.format(a1_cols[0]))
            df.rename(columns={a1_cols[0]:'A1'}, inplace=True)
        else:
            print('Unable to determine A1 column.')            

    if 'A2' not in df.columns:
        a2_cols = []
        if ('ALLELE0' in df.columns):
            a2_cols = ['ALLELE0']
        a2_cols += list(c for c in df.columns if str(c).lower().startswith('a2') and ('freq' not in  str(c).lower()) and ('frq' not in str(c).lower()))
        a2_cols += list(c for c in df.columns if str(c).lower().startswith('allele') and str(c).endswith('2'))
        a2_cols += list(c for c in df.columns if str(c).lower().startswith('other') and str(c).lower().endswith('allele'))
        a2_cols += list(c for c in df.columns if str(c).lower().startswith('ref') and str(c).lower().endswith('allele'))
        if len(a2_cols):
            if len(a2_cols) > 1:
                print('Warning: found multiple possible columns containing A2 : {}'.format(a1_cols))
            print('Assuming "{}" is the A2 column'.format(a2_cols[0]))
            df.rename(columns={a2_cols[0]:'A2'}, inplace=True)
        else:
            print('Unable to determine A2 column.')
            
    if 'BETA' not in df.columns:
        beta_cols = list(c for c in df.columns if 'beta' in str(c).lower())
        beta_cols += list(c for c in df.columns if 'effect' in str(c).lower() and not 'allele' in str(c).lower())
        if len(beta_cols):
            print('Assuming "{}" is the BETA column'.format(beta_cols[0]))
            df.rename(columns={beta_cols[0]: 'BETA'}, inplace=True)

    if 'SD' not in df.columns:
        sd_cols = list(c for c in df.columns if str(c).lower() in ['sd','std','stderr','stdev'])
        sd_cols += list(c for c in df.columns if 'error' in str(c).lower() or 'deviation' in str(c).lower())
        if len(sd_cols):
            if len(sd_cols) > 1:
                print('Warning: found multiple possible columns containing SD: {}'.format(sd_cols))
            print('Assuming "{}" is the P column'.format(sd_cols[0]))
            df.rename(columns={sd_cols[0]:'SD'}, inplace=True)
            
            
    if 'FRQ' not in df.columns:
        frq_cols = list(c for c in df.columns if ('freq' in str(c).lower()) or ('frq' in str(c).lower()) )
        if len(frq_cols):
            print('Assuming "{}" is the FRQ column'.format(frq_cols[0]))
            df.rename(columns={frq_cols[0]:'FRQ'}, inplace=True)
            
    if 'P' not in df.columns:
        pv_cols = []
        pv_cols += list(c for c in df.columns if str(c).lower() == 'p')
        pv_cols += list(c for c in df.columns if (str(c).lower().startswith('p')) and ('val' in c))
        if 'P_BOLT_LMM_INF' in df.columns:
            pv_cols += ['P_BOLT_LMM_INF']
        if 'P_LINREG' in df.columns:
            pv_cols +=  ['P_LINREG']
        if len(pv_cols):
            if len(pv_cols) > 1:
                print('Warning: found multiple possible columns containing p-values: {}'.format(pv_cols))
            print('Assuming "{}" is the P column'.format(pv_cols[0]))
            df.rename(columns={pv_cols[0]:'P'}, inplace=True)

    if 'N' not in df.columns:
        n_cols = []
        n_cols = list(c for c in df.columns if str(c).lower() == 'n')
        n_cols += list(c for c in df.columns if str(c).lower().startswith('n_total'))
        if len(n_cols):
            if len(n_cols) > 1:
                print('Warning: found multiple possible columns containing N: {}'.format(n_cols))
            print('Assuming "{}" is the N column'.format(n_cols[0]))
            df.rename(columns={n_cols[0]:'N'}, inplace=True)


    # ensure A1,A2 are upper case - otherwise QC script disregards them
    try:
        df['A1'] = df['A1'].str.upper()
    except KeyError as e:
        print('Error: could not determine A1 column. available columns:{}'.format(df.columns.tolist()))
        raise e

    # ensure A1,A2 are upper case - otherwise QC script disregards them
    try:
        df['A2'] = df['A2'].str.upper()
    except KeyError as e:
        print('Error: could not determine A2 column. available columns:{}'.format(df.columns.tolist()))
        raise e
    
    if 'OR' in df.columns and 'BETA' in df.columns:
        print('Warning: Found both OR and BETA columns, dropping the OR column')
        df.drop(['OR'], axis=1, inplace=True)

    # drop irrelevant columns
    found_cols = list(col for col in df.columns if col in rename_cols.values())

    df = df[found_cols]
    df = df.dropna(axis=1,how='all')

    return df

def validate(df):
    # put sanity checks in here
    sum_assoc = (df['P'] < 1e-8).sum()
    min_p = df['P'].min()

    print('the lowest p-value is {}'.format(min_p))

    sum_rsid = df['SNP'].str.startswith('rs').sum()

    if 'N' not in df.columns:
        print('Warning: could not determine sample size column (N)')

    assert sum_assoc > 0, 'Error: there are no genome-wide significant variants (p < 1e-8)'
    assert sum_rsid > 0, 'Error: there are no variants with rsids'




def get_args():

    p = ArgumentParser()

    p.add_argument('-i', '--infile', required=True)
    p.add_argument('-o', '--outfile', required=True)

    args = p.parse_args()
    return(args)


def main():

    args = get_args()
    ss = pd.read_csv(args.infile, sep='\t')
    ss = cleanup_summary_statistics(ss)

    validate(ss)

    ss.to_csv(args.outfile, sep='\t', index=False)


if __name__ == '__main__':
    main()






