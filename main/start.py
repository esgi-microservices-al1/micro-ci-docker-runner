from main.src.service.Runner import Runner


if __name__ == "__main__" :
    runner = Runner()

    runner.run("touch test", False)
    runner.run("ls", True)

    runner.stop()
