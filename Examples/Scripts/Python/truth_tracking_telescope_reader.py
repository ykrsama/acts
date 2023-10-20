#!/usr/bin/env python3

from pathlib import Path

import acts
import acts.examples

from truth_tracking_kalman import runTruthTrackingKalman

u = acts.UnitConstants

if "__main__" == __name__:
    detector, trackingGeometry, decorators = acts.examples.TelescopeDetector.create(
        bounds=[200, 200],
        positions=[30, 60, 90, 120, 150, 180, 210, 240, 270],
        stereos=[0] * 9,
    )

    srcdir = Path(__file__).resolve().parent.parent.parent.parent

    field = acts.ConstantBField(acts.Vector3(0, 0, 2 * u.T))

    from acts.examples import (
        RootSimHitReader,
        RootParticleReader,
    )
    s = acts.examples.Sequencer(
        numThreads=-1, logLevel=acts.logging.INFO
    )
    s.addReader(
        RootSimHitReader(
            level=acts.logging.INFO,
            filePath="telescope_simulation/fatras/hits.root",
            treeName="hits",
            simHitCollection="simhits",
        )
    )
    s.addReader(
        RootParticleReader(
            level=acts.logging.INFO,
            filePath="telescope_simulation/fatras/particles.root",
            particleCollection="particles",
            orderedEvents=False,
        )
    )


    runTruthTrackingKalman(
        trackingGeometry,
        field,
        digiConfigFile=srcdir
        / "Examples/Algorithms/Digitization/share/default-smearing-config-telescope.json",
        outputDir=Path.cwd(),
        s=s,
        inputParticlePath=srcdir
        / "telescope_simulation/fatras/particles.root"
    ).run()
