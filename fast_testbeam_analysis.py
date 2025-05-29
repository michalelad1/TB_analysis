import init_funcs
import tb_helpers_v2025 as tb_util


def test_func(df):
    print(df)


if __name__ == "__main__":

    # tests only!
    init_funcs.init_process(".root", test_func, root_tree="Hits")
    init_funcs.init_process(".parquet", test_func)

