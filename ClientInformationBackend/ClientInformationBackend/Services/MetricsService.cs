using ClientInformationBackend.Core.Constants;
using GRYLibrary.Core.APIServer.BaseServices;
using GRYLibrary.Core.APIServer.Settings;
using GRYLibrary.Core.APIServer.Services.Logger;
using GRYLibrary.Core.Logging.GRYLogger;
using System.Diagnostics.Metrics;
using System;
using System.Threading;

namespace ClientInformationBackend.Core.Services
{
    public class MetricsService : IteratingBackgroundService, IMetricsService
    {
        private readonly Meter _AmountOfDataSetsMeter;
        public Counter<long> MetricAmountOfDataSets { get; private set; }
        public TimeSpan AdditionalDelay { get; set; } = TimeSpan.FromSeconds(20);
        // The log is taken as IServerLog and not as IGRYLog, because IServerLog is the one which is
        // registered in the dependency-injection-container. Asking for IGRYLog compiles, but the application
        // then does not start ("Unable to resolve service for type ...").
        public MetricsService(IApplicationConstants<CodeUnitSpecificConstants> constants, IServerLog logger) : base(constants.ExecutionMode, logger.Logger)
        {
            this._AmountOfDataSetsMeter = new Meter(CodeUnitSpecificConstants.MetricAmountOfDataSetsName);
            this.MetricAmountOfDataSets = this._AmountOfDataSetsMeter.CreateCounter<long>(CodeUnitSpecificConstants.MetricAmountOfDataSetsName);
            this.Enabled = true;
        }

        public void CalculateHealthAndMetrics()
        {
            try
            {
                this.MetricAmountOfDataSets.Add(5);//TODO set actual value
            }
            catch (Exception exception)
            {
                this._Logger.Log("Error while calculating metrics", exception);
            }
        }

        protected override void Run()
        {
            Thread.Sleep(this.AdditionalDelay);
            this.CalculateHealthAndMetrics();
        }
    }
}
