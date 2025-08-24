import argparse
import markovify
import MeCab


def wakati_text_format(input_file: str, output_file: str) -> None:
    """テキストを分かち書きして、処理した内容をファイルとして出力する関数

    Args:
        input_file (str): 分かち書きをする対象となるファイル名
        output_file (str): 分かち書きした結果を出力するファイル名
    """
    mcb = MeCab.Tagger("-Owakati")

    with open(input_file, "r", encoding="utf-8") as infile:
        with open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                result = mcb.parse(line)
                outfile.write(result)


def generate_markov_chain_text(input_file: str, count: int) -> None:
    """分かち書きをしたファイルを元に、マルコフ連鎖で文章を生成して標標準出に出力する関数

    Args:
        input_file (str): 分かち書きしたテキストが記載されたファイル名
        count (int): 文章を生成する回数
    """
    with open(input_file, "r", encoding="utf-8") as wktfile:
        wakati_text = wktfile.read()
        text_model = markovify.NewlineText(wakati_text, state_size=2)

        # count で指定した分の繰り返し生成のための for 文
        for _ in range(count):
            sentence = text_model.make_short_sentence(100, 20, tries=120).replace(" ", "")
            print(sentence)


def main(filename: str, wakati_filename: str, only_markov: bool, count: int) -> None:
    """テキストファイルから、マルコフ連鎖を用いて文章生成を行う関数

    Args:
        filename (str): マルコフ連鎖の元になるテキストファイル名
        wakati_filename (str): 分かち書きしたテキストファイル名
        only_markov (bool): マルコフ連鎖のみを行うか否か
        count (int): 文章生成をする回数
    """

    if not only_markov:
        wakati_text_format(filename, wakati_filename)
    else:
        # マルコフ連鎖のためのファイル名変数を共通化する。
        # only_markov モードの場合、wakati_filename は特に使わないため、特に問題にはならない想定。
        wakati_filename = filename

    generate_markov_chain_text(wakati_filename, count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        required=True,
        help="マルコフ連鎖の元になるテキストファイル名 (--markov-only オプションを指定する場合は、分かち書きされたファイル名を指定)",
    )
    parser.add_argument(
        "-w",
        "--wakati-filename",
        default="wakati.txt",
        help="処理過程で出力する、分かち書きのテキストファイル名 (--markov-only オプションを指定している場合は使用しない)",
    )
    parser.add_argument(
        "-m", "--markov-only", action="store_true", help="マルコフ連鎖のみを行う (分かち書き処理を行わない)"
    )
    parser.add_argument(
        "-c", "--count", type=int, default=1, help="文章生成を行う回数を指定する (何も指定しなければ 1 回のみ)"
    )

    args = parser.parse_args()

    main(args.filename, args.wakati_filename, args.only_markov, args.count)
