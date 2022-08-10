import click

@click.command()
@click.option('-num')
def pred(num):
    print(num)

# 如果是多个，则
'''
@click.command()
@click.option('-i')
@click.option('-o')
def pred(i, o):
'''
if __name__ == '__main__':
    pred()